"""
Database Access Layer Infrastructure.
Exposes tables, schema mappings, and contextual database session injection handles.
"""
from app.database.base_class import Base
from app.database.session import get_db, engine, SessionLocal
from app.database.models import Trip, CachedLocation

__all__ = ["Base", "get_db", "engine", "SessionLocal", "Trip", "CachedLocation"]
