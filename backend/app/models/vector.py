from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, ARRAY, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.db.database import Base

class NovelEmbedding(Base):
    __tablename__ = "novel_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    novel_id = Column(Integer, ForeignKey("novels.id"), nullable=False)
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=True)
    content_type = Column(String, nullable=False)  # 'chapter', 'character', 'event', etc.
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1024))  # 阿里云text-embedding-v4模型输出1024维向量
    meta_data = Column(String)  # JSON string for additional metadata (renamed to avoid SQLAlchemy reserved keyword)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    novel = relationship("Novel")
    chapter = relationship("Chapter")