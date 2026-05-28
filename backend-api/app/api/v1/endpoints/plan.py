from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db, verify_api_client
from app.schemas.plan import TripGenerationRequest
from app.schemas.trip_dashboard import TripDashboardSchema
from app.services.trip_service import TripOrchestrationService

router = APIRouter()

@router.post("", response_model=TripDashboardSchema, status_code=status.HTTP_201_CREATED)
async def generate_new_trip_itinerary(
    payload: TripGenerationRequest,
    db: AsyncSession = Depends(get_db),
    _client_key: str = Depends(verify_api_client)
) -> TripDashboardSchema:
    """
    Accepts full group profile specifications matching UI inputs, orchestrates 
    the multi-agent CrewAI processing loop via Groq, saves the result, and returns 
    the complete customized dashboard schema response.
    """
    service = TripOrchestrationService(db)
    generated_dashboard = await service.create_optimized_trip_plan(payload)
    return generated_dashboard
