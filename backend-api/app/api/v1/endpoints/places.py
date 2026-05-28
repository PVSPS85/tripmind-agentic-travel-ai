from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db
from app.schemas.places import AutocompleteSearchResponse
from app.tools.places_api import GeoapifyPlacesClient
from app.database.repository import DatabaseRepository

router = APIRouter()

@router.get("/autocomplete", response_model=AutocompleteSearchResponse, status_code=status.HTTP_200_OK)
async def get_location_autocomplete_suggestions(
    query: str = Query(..., min_length=2, description="City query string (e.g., 'Goa')"),
    db: AsyncSession = Depends(get_db)
) -> AutocompleteSearchResponse:
    """
    Provides real-time location suggestion lookups for the landing page destination search field.
    Caches historical lookup records inside Supabase to minimize third-party API quotas.
    """
    repo = DatabaseRepository(db)
    
    # Attempt to fetch matching records from local persistent database cache layer
    cached_records = await repo.search_cached_locations(query)
    if cached_records:
        return AutocompleteSearchResponse(query=query, results=cached_records)
    
    # Fallback to direct external API integration lookup upon cache miss
    external_results = await GeoapifyPlacesClient.fetch_suggestions(query)
    
    # Save elements to database cache sequentially without interrupting return flows
    for item in external_results:
        await repo.create_cached_location(item)
        
    return AutocompleteSearchResponse(query=query, results=external_results)
