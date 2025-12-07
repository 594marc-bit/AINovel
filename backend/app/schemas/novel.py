from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.models.novel import NOVEL_STATUS_VALUES

# NovelStatus 类型用于 Pydantic
from enum import Enum

class NovelStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    COMPLETED = "completed"

class ChapterBase(BaseModel):
    title: str
    content: str

class ChapterCreate(ChapterBase):
    chapter_number: int
    is_ai_generated: Optional[bool] = False

class ChapterUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_ai_generated: Optional[bool] = None

class Chapter(ChapterBase):
    id: int
    novel_id: int
    chapter_number: int
    is_ai_generated: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class NovelBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: NovelStatus = NovelStatus.DRAFT
    is_public: bool = False

class NovelCreate(NovelBase):
    pass

class NovelUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[NovelStatus] = None
    is_public: Optional[bool] = None

class Novel(NovelBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    chapters: List[Chapter] = []

    class Config:
        from_attributes = True

class NovelList(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: NovelStatus
    is_public: bool
    created_at: datetime
    chapter_count: int = 0

    class Config:
        from_attributes = True