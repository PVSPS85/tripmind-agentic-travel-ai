import uuid
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class AIExplainability(BaseModel):
    reason_why: str = Field(..., description="The contextually generated 'Why this place' or 'Ideal for group' text line")
    best_time_to_visit: Optional[str] = Field(None, description="Optimal operational hours or season context details")

class ActivityItem(BaseModel):
    time_slot: str = Field(..., description="Morning, Afternoon, Evening operational bracket windows")
    activity_name: str = Field(..., description="Action title designation text string")
    description: str = Field(..., description="Complete narrative breakdown details")
    estimated_cost_inr: float = Field(default=0.0)
    explainability: AIExplainability

class DayItinerary(BaseModel):
    day_number: int
    date_string: str = Field(..., description="Format e.g., '15 Jun, 2026'")
    theme: str = Field(..., description="Focus theme statement for specific track matching day priorities")
    activities: List[ActivityItem]

class HotelRecommendation(BaseModel):
    name: str
    rating: float
    price_per_night_inr: float
    location_area: str
    amenities_tags: List[str]
    explainability: AIExplainability

class FoodRecommendation(BaseModel):
    restaurant_name: str
    cuisine_type: str
    rating: float
    dietary_suitability: str = Field(..., description="Veg / Non-Veg matching profile filters")
    estimated_cost_per_person_inr: float
    explainability: AIExplainability

class TransportSegment(BaseModel):
    mode: str = Field(..., description="Private Cab, Walking, Auto, Senior-friendly transfer")
    recommended_flow: str
    estimated_cost_inr: float

class WeatherInsight(BaseModel):
    expected_condition: str = Field(..., description="Monsoon rain thresholds, clear hot indices, etc.")
    packing_suggestions: List[str]
    adaptive_itinerary_note: str

class BudgetOptimizationBreakdown(BaseModel):
    allocated_hotels_total_inr: float
    allocated_food_total_inr: float
    allocated_activities_total_inr: float
    allocated_transport_total_inr: float
    remaining_buffer_inr: float
    summary_insight: str

class TripDashboardSchema(BaseModel):
    trip_id: uuid.UUID
    destination: str
    duration_days: int
    ai_optimization_summary: List[str] = Field(..., description="Bullets displaying how multi-agents structured output constraints")
    weather_pipeline: WeatherInsight
    budget_intelligence: BudgetOptimizationBreakdown
    hotels: List[HotelRecommendation]
    food_and_dining: List[FoodRecommendation]
    transportation: List[TransportSegment]
    itinerary: List[DayItinerary]
