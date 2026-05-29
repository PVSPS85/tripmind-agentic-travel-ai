from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import QueuePool, NullPool
from app.config import settings

# Determine if using SQLite or PostgreSQL
is_sqlite = "sqlite" in settings.DATABASE_URL

if is_sqlite:
    # SQLite: NullPool only, no connection pooling options
    db_url = settings.DATABASE_URL
    engine = create_async_engine(
        db_url,
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False},
        poolclass=NullPool
    )
else:
    # PostgreSQL: Disable prepared statement cache for PgBouncer compatibility
    # The ultimate fix for Supabase + asyncpg is to use the direct port (5432)
    # instead of the PgBouncer transaction port (6543).
    db_url = settings.DATABASE_URL.replace(":6543", ":5432")
    if "?" in db_url:
        db_url += "&prepared_statement_cache_size=0"
    else:
        db_url += "?prepared_statement_cache_size=0"

    if settings.ENVIRONMENT == "development":
        # PostgreSQL Development: use NullPool (no connection pooling)
        engine = create_async_engine(
            db_url,
            echo=settings.DEBUG,
            pool_pre_ping=True,
            poolclass=NullPool,
            connect_args={"statement_cache_size": 0}
        )
    else:
        # PostgreSQL Production: For Supabase PgBouncer, we MUST use NullPool
        # because PgBouncer already handles pooling in transaction mode.
        engine = create_async_engine(
            db_url,
            echo=settings.DEBUG,
            pool_pre_ping=True,
            poolclass=NullPool,
            connect_args={"statement_cache_size": 0}
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
