"""Database initialization script for PostgreSQL setup."""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.database.base import Base
from app.config import settings


async def init_db() -> None:
    """Initialize database with all tables from ORM models."""
    engine = create_async_engine(settings.database_url, echo=True)

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_db())
