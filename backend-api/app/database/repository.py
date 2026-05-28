import uuid
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Trip, CachedLocation
from app.schemas.places import PlaceSuggestionItem

class DatabaseRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db = db_session

    async def get_trip_by_id(self, trip_id: uuid.UUID) -> Optional[Trip]:
        statement = select(Trip).where(Trip.id == trip_id)
        result = await self.db.execute(statement)
        return result.scalars().first()

    async def save_trip_record(self, trip_obj: Trip) -> Trip:
        self.db.add(trip_obj)
        await self.db.flush()
        return trip_obj

    async def search_cached_locations(self, query: str) -> List[PlaceSuggestionItem]:
        # Simple structural lookup across location strings
        statement = select(CachedLocation).where(CachedLocation.search_query.ilike(f"%{query}%"))
        result = await self.db.execute(statement)
        records = result.scalars().all()
        
        return [
            PlaceSuggestionItem(
                display_name=r.display_name,
                city=r.search_query.capitalize(),
                state=None,
                country="India",
                lat=float(r.lat),
                lon=float(r.lon)
            ) for r in records
        ]

    async def create_cached_location(self, item: PlaceSuggestionItem) -> None:
        # Check existence safely first to ensure idempotent writes
        stmt = select(CachedLocation).where(CachedLocation.search_query == item.display_name.lower())
        exists_check = await self.db.execute(stmt)
        if exists_check.scalars().first():
            return
            
        cached_loc = CachedLocation(
            search_query=item.display_name.lower(),
            display_name=item.display_name,
            lat=item.lat,
            lon=item.lon
        )
        self.db.add(cached_loc)
        await self.db.flush()
