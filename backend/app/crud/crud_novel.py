from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.models.novel import Novel, Chapter
from app.schemas.novel import NovelCreate, NovelUpdate, ChapterCreate, ChapterUpdate

class CRUDNovel:
    async def get(self, db: AsyncSession, id: int) -> Optional[Novel]:
        result = await db.execute(
            select(Novel)
            .options(selectinload(Novel.chapters))
            .where(Novel.id == id)
        )
        return result.scalar_one_or_none()

    async def get_multi(
        self, db: AsyncSession, skip: int = 0, limit: int = 100, author_id: Optional[int] = None
    ) -> List[Novel]:
        query = select(Novel)
        if author_id:
            query = query.where(Novel.author_id == author_id)

        # Get count of chapters for each novel
        query = query.outerjoin(Chapter).group_by(Novel.id).add_columns(
            func.count(Chapter.id).label("chapter_count")
        )

        result = await db.execute(
            query.offset(skip).limit(limit).order_by(Novel.created_at.desc())
        )

        novels = []
        for row in result:
            novel = row[0]
            novel.chapter_count = row[1]
            novels.append(novel)

        return novels

    async def create(self, db: AsyncSession, obj_in: NovelCreate, author_id: int) -> Novel:
        db_obj = Novel(**obj_in.dict(), author_id=author_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: Novel, obj_in: NovelUpdate) -> Novel:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id: int) -> Optional[Novel]:
        result = await db.execute(select(Novel).where(Novel.id == id))
        obj = result.scalar_one_or_none()
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

class CRUDChapter:
    async def get(self, db: AsyncSession, id: int) -> Optional[Chapter]:
        result = await db.execute(select(Chapter).where(Chapter.id == id))
        return result.scalar_one_or_none()

    async def get_by_novel(
        self,
        db: AsyncSession,
        novel_id: int,
        skip: int = 0,
        limit: int = 100,
        before_chapter_id: Optional[int] = None
    ) -> List[Chapter]:
        query = select(Chapter).where(Chapter.novel_id == novel_id)

        # If before_chapter_id is provided, get chapters before it
        if before_chapter_id:
            # Get the chapter number of the specified chapter
            chapter_result = await db.execute(
                select(Chapter.chapter_number).where(Chapter.id == before_chapter_id)
            )
            chapter_number = chapter_result.scalar_one_or_none()
            if chapter_number:
                query = query.where(Chapter.chapter_number < chapter_number)

        result = await db.execute(
            query.order_by(Chapter.chapter_number.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: ChapterCreate, novel_id: int) -> Chapter:
        # Check if chapter number already exists
        existing = await db.execute(
            select(Chapter).where(
                Chapter.novel_id == novel_id,
                Chapter.chapter_number == obj_in.chapter_number
            )
        )
        if existing.scalar_one_or_none():
            raise ValueError(f"Chapter {obj_in.chapter_number} already exists")

        db_obj = Chapter(**obj_in.dict(), novel_id=novel_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: Chapter, obj_in: ChapterUpdate) -> Chapter:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id: int) -> Optional[Chapter]:
        result = await db.execute(select(Chapter).where(Chapter.id == id))
        obj = result.scalar_one_or_none()
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

    async def get_next_chapter_number(self, db: AsyncSession, novel_id: int) -> int:
        result = await db.execute(
            select(func.coalesce(func.max(Chapter.chapter_number), 0))
            .where(Chapter.novel_id == novel_id)
        )
        max_number = result.scalar()
        return (max_number or 0) + 1

crud_novel = CRUDNovel()
crud_chapter = CRUDChapter()