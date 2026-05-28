from pydantic import BaseModel, Field
from typing import List, Optional

class PlaceSuggestionItem(BaseModel):
    display_name: str = Field(..., description="Full descriptive location string for input UI dropdown selection")
    city: str = Field(..., description="Parsed localized operational target city entity")
    state: Optional[str] = Field(None, description="Regional fallback state context")
    country: str = Field(..., description="Sovereign operational container layer description")
    lat: float = Field(..., description="Geographic latitude position coordinate")
    lon: float = Field(..., description="Geographic longitude position coordinate")

class AutocompleteSearchResponse(BaseModel):
    query: str
    results: List[PlaceSuggestionItem] = Field(default=[])
