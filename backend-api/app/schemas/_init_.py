"""
Data Validation and Serialization Contracts (Pydantic Models).
Ensures incoming form inputs and downstream dashboard JSON objects match front-end contracts.
"""
from app.schemas.plan import TripGenerationRequest, TravelerBreakdown
from app.schemas.places import AutocompleteSearchResponse, PlaceSuggestionItem
from app.schemas.trip_dashboard import TripDashboardSchema

__all__ = [
    "TripGenerationRequest",
    "TravelerBreakdown",
    "AutocompleteSearchResponse",
    "PlaceSuggestionItem",
    "TripDashboardSchema",
]
