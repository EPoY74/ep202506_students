"""
DATABASE_URL = poctgresql+asyncpg://uk_bot_db_user:uk_bot_db_user@localhost:5432/uk_bot_db
"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import asyncpg


# DATABASE_URL = "sqlite+aiosqlite:///./test.db"  # Можно заменить на PostgreSQL
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/students"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
