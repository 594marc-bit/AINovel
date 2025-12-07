import asyncio
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine
from urllib.parse import urlparse
from app.core.config import settings

def parse_database_url(db_url: str):
    """Parse DATABASE_URL and extract connection parameters."""
    # Parse the URL using urllib.parse.urlparse
    parsed = urlparse(db_url)
    
    # Extract components
    user = parsed.username or "postgres"
    password = parsed.password or ""
    host = parsed.hostname or "localhost"
    port = parsed.port or 5432
    database = parsed.path.lstrip('/') or "postgres"
    
    return {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "database": database
    }

async def init_database():
    # Parse DATABASE_URL from settings
    db_params = parse_database_url(settings.DATABASE_URL)
    
    # Connect to PostgreSQL server (without specifying database)
    conn = await asyncpg.connect(
        host=db_params["host"],
        port=db_params["port"],
        user=db_params["user"],
        password=db_params["password"],
        database="postgres"  # Connect to default postgres database first
    )

    try:
        # Create database if it doesn't exist
        db_name = db_params["database"]
        await conn.execute(f"CREATE DATABASE {db_name}")
        print(f"Database '{db_name}' created successfully")
    except Exception as e:
        if "already exists" in str(e):
            print(f"Database '{db_params['database']}' already exists")
        else:
            print(f"Error creating database: {e}")
    finally:
        await conn.close()

    # Now connect to the target database to enable pgvector
    conn = await asyncpg.connect(
        host=db_params["host"],
        port=db_params["port"],
        user=db_params["user"],
        password=db_params["password"],
        database=db_params["database"]
    )

    try:
        # Enable pgvector extension
        await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        print("pgvector extension enabled successfully")
    except Exception as e:
        print(f"Error enabling pgvector: {e}")
    finally:
        await conn.close()

    # Create tables using SQLAlchemy
    from app.db.database import Base
    from app.models import User, Novel, Chapter, NovelEmbedding  # Import all models

    engine = create_async_engine(settings.DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Database tables created successfully")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_database())
