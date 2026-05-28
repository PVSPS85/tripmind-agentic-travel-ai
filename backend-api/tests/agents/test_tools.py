import pytest
from app.tools.serper_search import SerperSearchToolWrapper
from app.tools.weather_api import OpenWeatherToolWrapper

@pytest.mark.asyncio
async def test_serper_search_tool_fallback_structure() -> None:
    """
    Verifies that the live exploration tool gracefully drops back to 
    consistent mockup maps when operational API keys are omitted.
    """
    results = await SerperSearchToolWrapper.search_live_data(query="Goa night clubs", limit=2)
    assert isinstance(results, list)
    assert len(results) > 0
    assert "title" in results[0]
    assert "snippet" in results[0]
    assert "Mock Spot" in results[0]["title"]

@pytest.mark.asyncio
async def test_openweather_tool_fallback_structure() -> None:
    """
    Ensures climate lookup wrappers yield structured, adaptive packing lists 
    and mitigation statements under varying conditions.
    """
    climate_data = await OpenWeatherToolWrapper.fetch_climatology_summary(destination="Ooty")
    assert isinstance(climate_data, dict)
    assert "expected_condition" in climate_data
    assert "packing_suggestions" in climate_data
    assert "adaptive_itinerary_note" in climate_data
    assert isinstance(climate_data["packing_suggestions"], list)
    assert len(climate_data["packing_suggestions"]) >= 2
