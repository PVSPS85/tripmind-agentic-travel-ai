from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import QueuePool, NullPool
from app.config import settings

# Determine if using SQLite or PostgreSQL
is_sqlite = "sqlite" in settings.DATABASE_URL

if is_sqlite:
    # SQLite: NullPool only, no connection pooling options
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False},
        poolclass=NullPool
    )
elif settings.ENVIRONMENT == "development":
    # PostgreSQL Development: use NullPool (no connection pooling)
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        poolclass=NullPool
    )
else:
    # PostgreSQL Production: use QueuePool with connection pooling
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        poolclass=QueuePool,
        pool_size=10,
        max_overflow=20
    )

# Create async session factory for dependency injection
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency injection function providing async database sessions.
    Handles transaction commit/rollback and proper cleanup.
    """
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
