import uuid
import json
import sys
import traceback
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.repository import DatabaseRepository
from app.database.models import Trip
from app.schemas.plan import TripGenerationRequest
from app.schemas.trip_dashboard import TripDashboardSchema
from app.core.exceptions import ResourceNotFoundException, AgentExecutionException

# Dynamically inject the ai-agents folder into PYTHONPATH
ai_agents_path = Path(__file__).resolve().parent.parent.parent.parent / "ai-agents"
if str(ai_agents_path) not in sys.path:
    sys.path.insert(0, str(ai_agents_path))

def _get_crew_orchestrator():
    """Lazy load CrewAI orchestrator only when needed."""
    from crew_orchestrator import TripCrewOrchestrator
    return TripCrewOrchestrator

class TripOrchestrationService:
    def __init__(self, db_session: AsyncSession) -> None:
        self.repo = DatabaseRepository(db_session)

    async def create_optimized_trip_plan(self, request: TripGenerationRequest) -> TripDashboardSchema:
        db_trip = Trip(
            destination=request.destination,
            start_date=str(request.start_date),
            end_date=str(request.end_date),
            budget_inr=request.budget_inr,
            user_inputs=request.model_dump(mode="json"),
            generated_itinerary=None
        )
        db_trip = await self.repo.save_trip_record(db_trip)
        
        try:
            # Format inputs to match what ai-agents expects
            budget_mode = "Moderate"
            if request.budget_inr >= 150000:
                budget_mode = "Luxury"
            elif request.budget_inr >= 80000:
                budget_mode = "Premium"
            elif request.budget_inr < 40000:
                budget_mode = "Budget"
                
            trip_inputs = {
                "destination": request.destination,
                "startDate": str(request.start_date),
                "endDate": str(request.end_date),
                "kids": request.travelers.kids,
                "adults": request.travelers.adults,
                "seniors": request.travelers.seniors,
                "budgetMode": budget_mode,
                "foodPref": request.food_preference,
                "travelStyle": request.travel_style,
                "interests": request.interests
            }
            
            OrchestratorClass = _get_crew_orchestrator()
            orchestrator = OrchestratorClass()
            
            # Run the synchronous plan_trip in a thread to avoid blocking the event loop
            import asyncio
            raw_agent_json_output = await asyncio.to_thread(orchestrator.plan_trip, trip_inputs)
            
            # If the orchestrator returned an error dict (non-fallback), use it anyway
            # since the orchestrator already builds rich fallback data
            if isinstance(raw_agent_json_output, dict) and "error" in raw_agent_json_output:
                if "details" in raw_agent_json_output and not raw_agent_json_output.get("itinerary"):
                    # The crew failed completely and didn't produce a fallback plan
                    # Build one using the orchestrator's offline builder
                    raw_agent_json_output = orchestrator._build_offline_fallback_plan(
                        trip_inputs, 
                        raw_agent_json_output.get("details", "Unknown error")
                    )
                    raw_agent_json_output["status"] = "offline_fallback"
                    
        except Exception as err:
            # Instead of raising an HTTP error, build a rich offline fallback plan
            print(f"[TripMind] Agent execution failed, using offline fallback: {err}")
            traceback.print_exc()
            try:
                OrchestratorClass = _get_crew_orchestrator()
                orchestrator = OrchestratorClass()
                raw_agent_json_output = orchestrator._build_offline_fallback_plan(
                    trip_inputs, str(err)
                )
                raw_agent_json_output["status"] = "offline_fallback"
            except Exception as fallback_err:
                print(f"[TripMind] Even fallback failed: {fallback_err}")
                raise AgentExecutionException(
                    detail=f"Agent generation and fallback both failed: {str(err)}"
                )

        # Ensure required fields exist with sensible defaults
        if "destination" not in raw_agent_json_output:
            raw_agent_json_output["destination"] = request.destination
        if "duration_days" not in raw_agent_json_output:
            delta = (request.end_date - request.start_date).days
            raw_agent_json_output["duration_days"] = max(1, min(delta, 7))
        if "ai_optimization_summary" not in raw_agent_json_output:
            raw_agent_json_output["ai_optimization_summary"] = ["AI-generated travel plan"]
        if "weather_pipeline" not in raw_agent_json_output:
            raw_agent_json_output["weather_pipeline"] = {
                "expected_condition": "Pleasant weather expected",
                "packing_suggestions": ["Comfortable walking shoes", "Light layers"],
                "adaptive_itinerary_note": "Standard weather conditions."
            }
        if "budget_intelligence" not in raw_agent_json_output:
            raw_agent_json_output["budget_intelligence"] = {
                "allocated_hotels_total_inr": request.budget_inr * 0.45,
                "allocated_food_total_inr": request.budget_inr * 0.20,
                "allocated_activities_total_inr": request.budget_inr * 0.10,
                "allocated_transport_total_inr": request.budget_inr * 0.15,
                "remaining_buffer_inr": request.budget_inr * 0.10,
                "summary_insight": "Budget allocated using standard travel ratios."
            }
        for key in ["hotels", "food_and_dining", "transportation", "itinerary"]:
            if key not in raw_agent_json_output:
                raw_agent_json_output[key] = []
        if "extra_activities" not in raw_agent_json_output:
            raw_agent_json_output["extra_activities"] = []

        db_trip.generated_itinerary = raw_agent_json_output
        await self.repo.save_trip_record(db_trip)

        return TripDashboardSchema(trip_id=db_trip.id, **raw_agent_json_output)

    async def get_historical_trip(self, trip_id: uuid.UUID) -> TripDashboardSchema:
        db_trip = await self.repo.get_trip_by_id(trip_id)
        if not db_trip or not db_trip.generated_itinerary:
            raise ResourceNotFoundException(detail="The requested trip configuration dashboard was not found.")
        return TripDashboardSchema(trip_id=db_trip.id, **db_trip.generated_itinerary)

    async def re_execute_agent_pipeline(self, trip_id: uuid.UUID) -> TripDashboardSchema:
        db_trip = await self.repo.get_trip_by_id(trip_id)
        if not db_trip:
            raise ResourceNotFoundException(detail="Target trip context mapping parameters unavailable.")
            
        request_context = TripGenerationRequest(**db_trip.user_inputs)
        return await self.create_optimized_trip_plan(request_context)
