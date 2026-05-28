"""
API Endpoints Container.
Exposes the individual functional routers mapped directly to frontend interfaces.
"""
from app.api.v1.endpoints.places import router as places_router
from app.api.v1.endpoints.plan import router as plan_router
from app.api.v1.endpoints.trips import router as trips_router

__all__ = ["places_router", "plan_router", "trips_router"]
