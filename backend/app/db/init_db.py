import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from app.db.database import Base

async def init_db():
    # Import all models here to ensure they are registered
    from app.models import user, novel  # Import model modules

    engine = create_async_engine(settings.DATABASE_URL, echo=True)

    async with engine.begin() as conn:
        # Drop all tables if they exist (for development)
        # await conn.run_sync(Base.metadata.drop_all)

        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

    print("Database initialized successfully!")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())