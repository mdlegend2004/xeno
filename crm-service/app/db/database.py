"""
database.py — Async SQLAlchemy engine + session factory.

Design notes:
  - We use asyncpg as the driver (postgresql+asyncpg://...)
  - expire_on_commit=False prevents SQLAlchemy from issuing lazy-load
    SELECT after a commit, which would fail in async context
  - get_db() is a FastAPI dependency that yields a session per request
    and guarantees cleanup even on errors
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/brewco")

# pool_pre_ping=True: validates connections before use (handles DB restarts)
engine = create_async_engine(
    DATABASE_URL,
    echo=False,          # set True during development to log SQL
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# expire_on_commit=False is CRITICAL for async — prevents implicit lazy loads
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


async def get_db():
    """FastAPI dependency: yields an async DB session, closes on exit."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
