import uuid
import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.repository import DatabaseRepository
from app.database.models import Trip
from app.schemas.plan import TripGenerationRequest
from app.schemas.trip_dashboard import TripDashboardSchema
from app.core.exceptions import ResourceNotFoundException, AgentExecutionException

# Forward-declaration signature helper for our CrewAI orchestrator execution mapping layer
# Implemented fully in subsequent agent module sequence files
from app.agents.crew import TripMindAgentCrewOrchestrator

class TripOrchestrationService:
    def __init__(self, db_session: AsyncSession) -> None:
        self.repo = DatabaseRepository(db_session)

    async def create_optimized_trip_plan(self, request: TripGenerationRequest) -> TripDashboardSchema:
        # 1. Initialize persistent structural record container
        db_trip = Trip(
            destination=request.destination,
            start_date=str(request.start_date),
            end_date=str(request.end_date),
            budget_inr=request.budget_inr,
            user_inputs=request.model_dump(mode="json"),
            generated_itinerary=None
        )
        db_trip = await self.repo.save_trip_record(db_trip)
        
        # 2. Invoke multi-agent execution cycle (CrewAI orchestrated with low latency Groq inference maps)
        try:
            orchestrator = TripMindAgentCrewOrchestrator(request_params=request, trip_uuid=db_trip.id)
            raw_agent_json_output = await orchestrator.run_orchestration_loop()
        except Exception as err:
            throw_msg = f"Multi-Agent generation layer execution encountered structural failure: {str(err)}"
            raise AgentExecutionException(detail=throw_msg)

        # 3. Commit structured operational dictionary outputs directly back into DB cache layers
        db_trip.generated_itinerary = raw_agent_json_output
        await self.repo.save_trip_record(db_trip)

        return TripDashboardSchema(trip_id=db_trip.id, **raw_agent_json_output)

    async def get_historical_trip(self, trip_id: uuid.UUID) -> TripDashboardSchema:
        db_trip = await self.repo.get_trip_by_id(trip_id)
        if not db_trip or not db_trip.generated_itinerary:
            raise ResourceNotFoundException(detail="The requested trip configuration dashboard was not found.")
        return TripDashboardSchema(trip_id=db_trip.id, **db_trip.generated_itinerary)

    async def re-execute_agent_pipeline(self, trip_id: uuid.UUID) -> TripDashboardSchema:
        db_trip = await self.repo.get_trip_by_id(trip_id)
        if not db_trip:
            raise ResourceNotFoundException(detail="Target trip context mapping parameters unavailable.")
            
        # Re-parse context models directly from saved execution snapshot structures
        request_context = TripGenerationRequest(**db_trip.user_inputs)
        
        orchestrator = TripMindAgentCrewOrchestrator(request_params=request_context, trip_uuid=db_trip.id)
        refreshed_json = await orchestrator.run_orchestration_loop()
        
        db_trip.generated_itinerary = refreshed_json
        await self.repo.save_trip_record(db_trip)
        return TripDashboardSchema(trip_id=db_trip.id, **refreshed_json)
