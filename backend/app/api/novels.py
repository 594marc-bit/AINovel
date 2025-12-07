from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.schemas.novel import Novel, NovelCreate, NovelUpdate, NovelList, Chapter, ChapterCreate, ChapterUpdate
from app.crud import crud_novel, crud_chapter
from app.services.ai_service import ai_service
from app.services.vector_service import vector_service

router = APIRouter()

@router.post("/", response_model=Novel)
async def create_novel(
    novel: NovelCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new novel"""
    # For MVP, hardcode user_id = 1
    db_novel = await crud_novel.create(db, novel, author_id=1)
    return db_novel

@router.get("/", response_model=List[NovelList])
async def get_novels(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get list of novels"""
    # For MVP, hardcode author_id = 1
    novels = await crud_novel.get_multi(db, skip=skip, limit=limit, author_id=1)
    return novels

@router.get("/{novel_id}", response_model=Novel)
async def get_novel(
    novel_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a novel by ID"""
    novel = await crud_novel.get(db, id=novel_id)
    if not novel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Novel not found"
        )
    return novel

@router.put("/{novel_id}", response_model=Novel)
async def update_novel(
    novel_id: int,
    novel_update: NovelUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a novel"""
    novel = await crud_novel.get(db, id=novel_id)
    if not novel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Novel not found"
        )
    # For MVP, skip authorization check
    return await crud_novel.update(db, novel, novel_update)

@router.delete("/{novel_id}")
async def delete_novel(
    novel_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a novel"""
    novel = await crud_novel.delete(db, id=novel_id)
    if not novel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Novel not found"
        )
    return {"message": "Novel deleted successfully"}

# Chapter endpoints
@router.post("/{novel_id}/chapters", response_model=Chapter)
async def create_chapter(
    novel_id: int,
    chapter: ChapterCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new chapter"""
    # Verify novel exists
    novel = await crud_novel.get(db, id=novel_id)
    if not novel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Novel not found"
        )

    # Auto-generate chapter number if not provided
    if not hasattr(chapter, 'chapter_number') or chapter.chapter_number == 0:
        next_number = await crud_chapter.get_next_chapter_number(db, novel_id)
        chapter.chapter_number = next_number

    db_chapter = await crud_chapter.create(db, chapter, novel_id=novel_id)

    # 生成章节内容的向量并存储
    try:
        await vector_service.index_chapter(db, db_chapter.id)
    except Exception as e:
        # 记录错误但不影响章节创建
        print(f"Error indexing chapter {db_chapter.id}: {e}")

    return db_chapter

@router.get("/{novel_id}/chapters", response_model=List[Chapter])
async def get_chapters(
    novel_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get chapters of a novel"""
    # Verify novel exists
    novel = await crud_novel.get(db, id=novel_id)
    if not novel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Novel not found"
        )
    return await crud_chapter.get_by_novel(db, novel_id, skip=skip, limit=limit)

@router.put("/chapters/{chapter_id}", response_model=Chapter)
async def update_chapter(
    chapter_id: int,
    chapter_update: ChapterUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a chapter"""
    chapter = await crud_chapter.get(db, id=chapter_id)
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )

    # 先保存章节更新（已经在 crud_chapter.update 中 commit）
    updated_chapter = await crud_chapter.update(db, chapter, chapter_update)

    # 使用新的事务处理向量更新
    try:
        from sqlalchemy.orm import sessionmaker
        from app.db.database import engine
        AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with AsyncSessionLocal() as vector_db:
            # 删除旧的向量记录（如果有）
            from sqlalchemy import delete
            from app.models.vector import NovelEmbedding
            await vector_db.execute(
                delete(NovelEmbedding).where(NovelEmbedding.chapter_id == chapter_id)
            )
            await vector_db.flush()

            # 创建新的向量记录
            await vector_service.index_chapter(vector_db, updated_chapter.id, commit=True)
    except Exception as e:
        # 记录错误但不影响章节更新
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error re-indexing chapter {chapter_id}: {e}")
        # 向量更新失败不影响章节内容的更新

    return updated_chapter

@router.delete("/chapters/{chapter_id}")
async def delete_chapter(
    chapter_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a chapter"""
    # 先删除相关的向量记录
    try:
        from sqlalchemy import delete
        from app.models.vector import NovelEmbedding
        await db.execute(
            delete(NovelEmbedding).where(NovelEmbedding.chapter_id == chapter_id)
        )
        # 不在这里commit，让crud_chapter.delete统一处理
    except Exception as e:
        # 记录错误但不影响章节删除
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error deleting embeddings for chapter {chapter_id}: {e}")

    chapter = await crud_chapter.delete(db, id=chapter_id)
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )
    return {"message": "Chapter deleted successfully"}