import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings

async def init_database():
    # Create tables using SQLAlchemy
    from app.db.database import Base
    from app.models import User, Novel, Chapter  # Import models without vector for now

    engine = create_async_engine(settings.DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Database tables created successfully")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_database())