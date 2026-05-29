import uuid
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class AIExplainability(BaseModel):
    reason_why: str = Field(..., description="The contextually generated 'Why this place' or 'Ideal for group' text line")
    best_time_to_visit: Optional[str] = Field(None, description="Optimal operational hours or season context details")

class ActivityItem(BaseModel):
    time_slot: str = Field(..., description="Morning, Afternoon, Evening operational bracket windows")
    start_time: str = Field(default="", description="Specific start time like '14:00' or '09:30'")
    activity_name: str = Field(..., description="Action title designation text string")
    description: str = Field(..., description="Complete narrative breakdown details")
    estimated_cost_inr: float = Field(default=0.0)
    target_age_group: str = Field(default="All ages", description="E.g., 'Families', 'Adults only', 'Seniors'")
    walking_effort: str = Field(default="Low walk", description="E.g., 'Low walk', 'Moderate walk'")
    energy_level: str = Field(default="Relaxed", description="E.g., 'Relaxed', 'Active'")
    transit_estimate: str = Field(default="", description="E.g., '🚗 8 min • Free'")
    image_url: Optional[str] = Field(None, description="Unsplash source URL placeholder")
    explainability: Optional[AIExplainability] = Field(default=None)

class ExtraActivityItem(BaseModel):
    activity_name: str
    image_url: Optional[str] = Field(None, description="Unsplash source URL placeholder")
    rating: float = Field(default=4.0)
    category: str = Field(default="Experience", description="E.g., 'Heritage • Fort', 'Shopping & culture'")
    target_age_group: str = Field(default="All ages")
    walking_effort: str = Field(default="Moderate walk")
    energy_level: str = Field(default="Balanced")
    duration: str = Field(default="2 hrs", description="E.g., '1.5 hrs'")
    best_time: str = Field(default="Morning", description="E.g., 'Morning'")
    estimated_cost_inr: float = Field(default=0.0)
    tags: List[str] = Field(default=[], description="E.g., ['Heritage', 'Hidden gem']")
    explainability: Optional[AIExplainability] = Field(default=None)

class DayItinerary(BaseModel):
    day_number: int
    date_string: str = Field(..., description="Format e.g., '15 Jun, 2026'")
    theme: str = Field(..., description="Focus theme statement for specific track matching day priorities")
    day_energy_badge: str = Field(default="Balanced", description="E.g., 'Relaxed', 'Balanced', 'Active'")
    weather_forecast: str = Field(default="Sunny 30°C", description="E.g., 'Partly cloudy 29°C'")
    activities: List[ActivityItem]

class HotelRecommendation(BaseModel):
    name: str
    rating: float = Field(default=4.0)
    price_per_night_inr: float = Field(default=0.0)
    location_area: str = Field(default="City Center")
    image_url: Optional[str] = Field(None, description="Unsplash source URL placeholder")
    amenities_tags: List[str] = Field(default=[])
    badges: List[str] = Field(default=[], description="E.g., ['Luxury', 'Senior-friendly']")
    explainability: Optional[AIExplainability] = Field(default=None)

class FoodRecommendation(BaseModel):
    restaurant_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    cuisine_type: str = Field(default="Local")
    rating: float = Field(default=4.0)
    dietary_suitability: str = Field(default="Both", description="Veg / Non-Veg matching profile filters")
    estimated_cost_per_person_inr: float = Field(default=500.0)
    distance: str = Field(default="5 km", description="E.g., 'Panjim • 8 km from hotel'")
    image_url: Optional[str] = Field(None, description="Unsplash source URL placeholder")
    explainability: Optional[AIExplainability] = Field(default=None)

    @property
    def display_name(self):
        return self.restaurant_name or self.name or "Restaurant"

class TransportSegment(BaseModel):
    mode: str = Field(..., description="E.g., 'Pre-booked AC cab'")
    duration: str = Field(default="", description="E.g., 'Full-day • 8 hrs'")
    cost_estimate: str = Field(default="", description="E.g., '₹2,800 / day'")
    badges: List[str] = Field(default=[], description="E.g., ['Best comfort', 'Senior-friendly']")
    explainability: Optional[AIExplainability] = Field(default=None)

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
    transportation: List[TransportSegment] = Field(default=[])
    extra_activities: List[ExtraActivityItem] = Field(default=[])
    itinerary: List[DayItinerary]
