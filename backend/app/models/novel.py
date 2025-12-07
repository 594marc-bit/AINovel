from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

# 定义 status 字段可能的值
NOVEL_STATUS_VALUES = ("draft", "published", "completed")

class Novel(Base):
    __tablename__ = "novels"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(*NOVEL_STATUS_VALUES, name="novel_status"), default="draft")
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    author = relationship("User")
    chapters = relationship("Chapter", back_populates="novel", cascade="all, delete-orphan")

class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    novel_id = Column(Integer, ForeignKey("novels.id"), nullable=False)
    chapter_number = Column(Integer, nullable=False)
    is_ai_generated = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    novel = relationship("Novel", back_populates="chapters")