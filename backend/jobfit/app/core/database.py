"""
Database session and connection management
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base 

from .config import get_settings

settings = get_settings()
#Create async engine 
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=10,
)

# Session factory
async_session_factory = async_sessionmaker(
    engine, 
    class_ = AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session    
    """
    async with async_session_factory() as session: 
        try: 
            yield session 
            await session.commit()
        except Exception: 
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db() -> None:
    """
    Initialize database (create tables if needed)
    """
    from app.models.base import Base
    async with engine.begin() as conn:
        pass 