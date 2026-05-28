from fastapi import APIRouter
from app.api.v1.endpoints import places, plan, trips

api_v1_router = APIRouter()

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
