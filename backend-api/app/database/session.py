from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import QueuePool, NullPool
from app.config import settings

# Create async engine with asyncpg driver for PostgreSQL/Supabase
# QueuePool is used in production; NullPool in development to avoid connection pool issues
pool_class = NullPool if settings.ENVIRONMENT == "development" else QueuePool

if settings.ENVIRONMENT == "development":
    # Development: use NullPool (no connection pooling)
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        poolclass=NullPool
    )
else:
    # Production: use QueuePool with connection pooling
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


