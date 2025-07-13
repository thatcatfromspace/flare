from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from fastapi import Depends
import redis
import os
import logging
from app.models import Base

# Setup logging
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:root@localhost:5432/flare"
)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


# Function to initialize models
async def init_models():
    """
    Initialize all models defined in models.py
    This ensures all tables are created in the database if they don't exist
    """
    try:
        # Create tables for all models that inherit from Base
        async with engine.begin() as conn:
            # This will create all tables that don't exist yet
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database models initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database models: {str(e)}")
        raise


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


def get_redis():
    r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    try:
        yield r
    finally:
        r.close()
