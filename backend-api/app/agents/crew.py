import os
import yaml
import json
from typing import Dict, Any
from pathlib import Path
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq

from app.config import settings
from app.schemas.plan import TripGenerationRequest

# 1. Import the specialized logic classes
from app.agents.specialized.profile_analyst import ProfileLogic
from app.agents.specialized.budget_optimizer import BudgetLogic

class TripMindAgentCrewOrchestrator:
    """
    Assembles the multi-agent execution pipeline, infuses specialized business logic,
    and binds low-latency Groq LLM instances for structured output generation.
    """
    def __init__(self, request_params: TripGenerationRequest, trip_uuid: Any) -> None:
        self.params = request_params
        self.trip_id = trip_uuid
        
        config_dir = Path(__file__).parent / "config"
        with open(config_dir / "agents.yaml", "r") as f:
            self.agents_config = yaml.safe_load(f)
        with open(config_dir / "tasks.yaml", "r") as f:
            self.tasks_config = yaml.safe_load(f)

        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name=settings.GROQ_MODEL_NAME,
            temperature=0.2
        )

    async def run_orchestration_loop(self) -> Dict[str, Any]:
        # 2. Execute specialized Python logic to compute hard constraints
        pacing_guardrails = ProfileLogic.determine_pacing_constraints(self.params.travelers.model_dump())
        budget_allocations = BudgetLogic.calculate_target_allocations(self.params.budget_inr)

        # 3. Instantiate specialized agents
        profile_analyst = Agent(
            config=self.agents_config["profile_analyst"],
            llm=self.llm,
            verbose=settings.DEBUG,
            allow_delegation=False
        )
        attraction_searcher = Agent(
            config=self.agents_config["attraction_searcher"],
            llm=self.llm,
            verbose=settings.DEBUG,
            allow_delegation=False
        )
        itinerary_designer = Agent(
            config=self.agents_config["itinerary_designer"],
            llm=self.llm,
            verbose=settings.DEBUG,
            allow_delegation=False
        )
        budget_optimizer = Agent(
            config=self.agents_config["budget_optimizer"],
            llm=self.llm,
            verbose=settings.DEBUG,
            allow_delegation=False
        )

        # 4. Inject computed data straight into the LLM context pool
        inputs = {
            "destination": self.params.destination,
            "kids": self.params.travelers.kids,
            "adults": self.params.travelers.adults,
            "seniors": self.params.travelers.seniors,
            "budget_inr": self.params.budget_inr,
            "food_preference": self.params.food_preference,
            "travel_style": self.params.travel_style,
            "interests": ", ".join(self.params.interests),
            
            # Smart context injections from profile_analyst logic
            "calculated_pace": pacing_guardrails["pace_label"],
            "max_active_hours": pacing_guardrails["max_active_hours"],
            "requires_accessibility": "Yes" if pacing_guardrails["requires_accessibility"] else "No",
            "is_child_friendly": "Yes" if pacing_guardrails["is_child_friendly"] else "No",
            
            # Smart context injections from budget_optimizer logic
            "hotel_budget_ceiling": budget_allocations["accommodation_target"],
            "food_budget_ceiling": budget_allocations["food_target"],
            "activity_budget_ceiling": budget_allocations["activity_target"],
            "transport_budget_ceiling": budget_allocations["transport_target"],
            "safety_buffer": budget_allocations["contingency_buffer"]
        }

        # 5. Define sequential execution tasks
        task_1 = Task(config=self.tasks_config["analyze_profile_task"], agent=profile_analyst)
        task_2 = Task(config=self.tasks_config["discover_attractions_task"], agent=attraction_searcher)
        task_3 = Task(config=self.tasks_config["construct_itinerary_task"], agent=itinerary_designer)
        task_4 = Task(config=self.tasks_config["optimize_budget_task"], agent=budget_optimizer)

        # 6. Kickoff Crew execution
        crew = Crew(
            agents=[profile_analyst, attraction_searcher, itinerary_designer, budget_optimizer],
            tasks=[task_1, task_2, task_3, task_4],
            process=Process.sequential,
            verbose=settings.DEBUG
        )

        raw_result = crew.kickoff(inputs=inputs)
        
        # 7. Standardize and return output format
        try:
            cleaned_str = str(raw_result).strip()
            if "```json" in cleaned_str:
                cleaned_str = cleaned_str.split("```json")[1].split("```")[0].strip()
            elif "```" in cleaned_str:
                cleaned_str = cleaned_str.split("```")[1].split("```")[0].strip()
            
            return json.loads(cleaned_str)
        except Exception:
            # Safe operational fallback schema
            return {
                "destination": self.params.destination,
                "duration_days": 3,
                "ai_optimization_summary": ["Fallback parsing active"],
                "weather_pipeline": {"expected_condition": "Mild", "packing_suggestions": [], "adaptive_itinerary_note": ""},
                "budget_intelligence": {
                    "allocated_hotels_total_inr": budget_allocations["accommodation_target"],
                    "allocated_food_total_inr": budget_allocations["food_target"],
                    "allocated_activities_total_inr": budget_allocations["activity_target"],
                    "allocated_transport_total_inr": budget_allocations["transport_target"],
                    "remaining_buffer_inr": budget_allocations["contingency_buffer"],
                    "summary_insight": "Enforced exact mathematical fallback bounds."
                },
                "hotels": [], "food_and_dining": [], "transportation": [], "itinerary": []
            }
