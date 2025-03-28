"""Database connection management."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import AsyncAdaptedQueuePool

from ..config import config

# Create the async engine
DATABASE_URL = (
    f"postgresql+asyncpg://{config.db.DB_USER}:{config.db.DB_PASSWORD}"
    f"@{config.db.DB_HOST}:{config.db.DB_PORT}/{config.db.DB_NAME}"
)

engine = create_async_engine(
    DATABASE_URL,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=config.db.DB_POOL_SIZE,
    max_overflow=config.db.DB_MAX_OVERFLOW,
    echo=config.debug,
)

# Create session factory
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise 