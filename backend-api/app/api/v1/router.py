from fastapi import APIRouter

def create_api_v1_router():
    """Create API v1 router with lazy endpoint loading."""
    api_v1_router = APIRouter()

    # Lazy import endpoints only when router is created
    from app.api.v1.endpoints import places, plan, trips

    # Register core application routers with distinct prefixes and descriptive documentation tags
    api_v1_router.include_router(
        places.router, 
        prefix="/places", 
        tags=["Location Autocomplete"]
    )
    api_v1_router.include_router(
        plan.router, 
        prefix="/plan", 
        tags=["Trip Engine Execution"]
    )
    api_v1_router.include_router(
        trips.router, 
        prefix="/trips", 
        tags=["Trip Dashboard Management"]
    )
    
    return api_v1_router

# Create router instance once at module import time
api_v1_router = create_api_v1_router()

