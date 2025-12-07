from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from app.models.novel import Novel, Chapter
from app.models.vector import NovelEmbedding
from app.core.config import settings
from typing import List, Optional
import json
import httpx
import logging

logger = logging.getLogger(__name__)

class VectorService:
    def __init__(self):
        # 直接使用阿里云DashScope API
        self.api_key = settings.EMBEDDING_API_KEY
        self.base_url = "https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding"
        self.model = settings.EMBEDDING_MODEL_NAME

    async def create_embedding(self, text: str) -> List[float]:
        """Create embedding for the given text using DashScope API directly"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "input": {
                "texts": [text]
            }
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json=data
                )
                response.raise_for_status()
                result = response.json()

                # 提取向量数据
                embeddings = result["output"]["embeddings"]
                if embeddings and len(embeddings) > 0:
                    return embeddings[0]["embedding"]
                else:
                    raise ValueError("No embeddings returned from API")

        except httpx.HTTPError as e:
            logger.error(f"HTTP error calling embedding API: {e}")
            raise
        except KeyError as e:
            logger.error(f"Error parsing embedding response: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating embedding: {e}")
            raise

    async def store_novel_embedding(
        self,
        db: AsyncSession,
        novel_id: int,
        content: str,
        content_type: str,
        chapter_id: Optional[int] = None,
        metadata: Optional[dict] = None,
        commit: bool = True
    ):
        """Store content embedding in vector database"""
        embedding = await self.create_embedding(content)

        novel_embedding = NovelEmbedding(
            novel_id=novel_id,
            chapter_id=chapter_id,
            content_type=content_type,
            content=content,
            embedding=embedding,
            meta_data=json.dumps(metadata) if metadata else None
        )

        db.add(novel_embedding)
        if commit:
            await db.commit()
        return novel_embedding

    async def search_similar_content(
        self,
        db: AsyncSession,
        novel_id: int,
        query_text: str,
        limit: int = 5
    ) -> List[NovelEmbedding]:
        """Search for similar content in the novel using vector similarity"""
        query_embedding = await self.create_embedding(query_text)

        # Using pgvector's <=> operator for cosine similarity
        sql = text("""
            SELECT * FROM novel_embeddings
            WHERE novel_id = :novel_id
            ORDER BY embedding <=> :query_embedding::vector
            LIMIT :limit
        """)

        result = await db.execute(
            sql,
            {
                "novel_id": novel_id,
                "query_embedding": query_embedding,
                "limit": limit
            }
        )

        return result.scalars().all()

    async def get_novel_context(
        self,
        db: AsyncSession,
        novel_id: int,
        chapter_id: Optional[int] = None
    ) -> str:
        """Get relevant context from previous chapters"""
        query = select(Chapter).where(Chapter.novel_id == novel_id)

        if chapter_id:
            # Get chapters before the current one
            query = query.where(Chapter.chapter_number <
                               select(Chapter.chapter_number).where(Chapter.id == chapter_id))

        query = query.order_by(Chapter.chapter_number.desc()).limit(3)

        result = await db.execute(query)
        chapters = result.scalars().all()

        if not chapters:
            return ""

        # Combine recent chapters for context
        context_parts = []
        for chapter in reversed(chapters):
            context_parts.append(f"第{chapter.chapter_number}章：{chapter.title}\n{chapter.content[:500]}...")

        return "\n\n".join(context_parts)

    async def index_chapter(self, db: AsyncSession, chapter_id: int, commit: bool = True):
        """Index a chapter for vector search"""
        # Get chapter with novel info
        result = await db.execute(
            select(Chapter, Novel).join(Novel).where(Chapter.id == chapter_id)
        )
        row = result.first()

        if not row:
            return

        chapter, novel = row

        # Store full chapter embedding
        await self.store_novel_embedding(
            db=db,
            novel_id=novel.id,
            chapter_id=chapter.id,
            content=f"{chapter.title}\n\n{chapter.content}",
            content_type="chapter",
            commit=False
        )

        # Extract and store character information (simplified)
        # In production, you might want to use NER models for better extraction
        if "人物：" in chapter.content or "角色：" in chapter.content:
            # Simple extraction - in production use more sophisticated methods
            await self.store_novel_embedding(
                db=db,
                novel_id=novel.id,
                chapter_id=chapter.id,
                content=chapter.content[:1000],  # First 1000 chars for character context
                content_type="characters",
                metadata={"chapter_title": chapter.title},
                commit=False
            )

        # 提交所有嵌入
        if commit:
            await db.commit()

vector_service = VectorService()