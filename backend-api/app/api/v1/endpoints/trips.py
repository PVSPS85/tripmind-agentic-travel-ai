import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db
from app.schemas.trip_dashboard import TripDashboardSchema
from app.services.trip_service import TripOrchestrationService

router = APIRouter()

@router.get("/{trip_id}", response_model=TripDashboardSchema, status_code=status.HTTP_200_OK)
async def get_saved_trip_details(
    trip_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
) -> TripDashboardSchema:
    """
    Fetches an already completed and cached multi-agent trip itinerary plan 
    directly from database records using its unique tracking UUID string identifier.
    """
    service = TripOrchestrationService(db)
    return await service.get_historical_trip(trip_id)


@router.post("/{trip_id}/regenerate", response_model=TripDashboardSchema, status_code=status.HTTP_200_OK)
async def regenerate_trip_components(
    trip_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
) -> TripDashboardSchema:
    """
    Triggers an on-demand re-execution pipeline of the agent layer for an existing trip record,
    refreshing tool lookups (like weather variations or live budget pricing shifts).
    """
    service = TripOrchestrationService(db)
    return await service.re-execute_agent_pipeline(trip_id)
