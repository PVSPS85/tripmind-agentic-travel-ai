import asyncio
from app.database.session import engine
from app.database.base_class import Base
from app.database.models import Trip, CachedLocation 

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())
