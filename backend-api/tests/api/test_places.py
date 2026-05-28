import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_autocomplete_endpoint_with_valid_seed_city() -> None:
    """
    Verifies that real-time lookup parameters successfully target seed cities 
    and deliver standardized geography models matching PlaceSuggestionItem schema constraints.
    """
    response = client.get("/api/v1/places/autocomplete?query=manali")
    assert response.status_code == 200
    
    payload = response.json()
    assert "query" in payload
    assert payload["query"] == "manali"
    assert isinstance(payload["results"], list)
    assert len(payload["results"]) > 0
    
    first_suggestion = payload["results"][0]
    assert "display_name" in first_suggestion
    assert "city" in first_suggestion
    assert "lat" in first_suggestion
    assert "lon" in first_suggestion
    assert first_suggestion["city"] == "Manali"

def test_autocomplete_endpoint_validation_error_on_short_query() -> None:
    """
    Ensures input constraint guardrails reject search requests with a 422 
    error if the string length falls below validation policies.
    """
    response = client.get("/api/v1/places/autocomplete?query=z")
    assert response.status_code == 422
