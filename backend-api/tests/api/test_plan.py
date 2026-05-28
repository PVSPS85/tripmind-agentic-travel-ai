import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_system_health_endpoint_returns_operational() -> None:
    """Verifies that foundational system health monitoring signals route clean 200 checks."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "operational"

def test_missing_payload_violates_generation_validation_bounds() -> None:
    """Ensures empty payloads trigger semantic validation rejections with a 422 error code."""
    response = client.post("/api/v1/plan", json={})
    assert response.status_code == 422
