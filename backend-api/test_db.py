import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.config import settings
from sqlalchemy import text
from app.database.models import Base

async def test():
    db_url = settings.DATABASE_URL.replace(":6543", ":5432")
    if "?" in db_url:
        db_url += "&prepared_statement_cache_size=0"
    else:
        db_url += "?prepared_statement_cache_size=0"
    
    print("URL:", db_url)
    engine = create_async_engine(
        db_url,
        poolclass=None,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("SUCCESS")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test())
