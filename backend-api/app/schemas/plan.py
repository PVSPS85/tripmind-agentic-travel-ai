from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import date

class TravelerBreakdown(BaseModel):
    kids: int = Field(default=0, ge=0, description="Count of travelers aged 0-17")
    adults: int = Field(default=1, ge=1, description="Count of travelers aged 18-49")
    seniors: int = Field(default=0, ge=0, description="Count of travelers aged 50+")

class TripGenerationRequest(BaseModel):
    destination: str = Field(..., min_length=2, max_length=100, examples=["Goa", "Manali", "Ooty"])
    start_date: date = Field(..., description="Trip start tracking date")
    end_date: date = Field(..., description="Trip termination date")
    travelers: TravelerBreakdown = Field(..., description="Demographic count split of group composition")
    budget_inr: float = Field(..., ge=5000, description="Total absolute multi-day group allocation limit in INR")
    food_preference: str = Field(..., description="Veg, Non-Veg, Vegan, or Both options matching dashboard filters")
    travel_style: str = Field(..., description="Relaxed, Adventurous, Balanced, Luxury, Corporate style bounds")
    interests: List[str] = Field(default=[], description="Selected interest chips like Beaches, Heritage, Nightlife")

    @field_validator("end_date")
    @classmethod
    def validate_date_sequence(cls, v: date, info) -> date:
        if "start_date" in info.data and v < info.data["start_date"]:
            raise ValueError("end_date cannot precede start_date")
        return v
