from crew_orchestrator import TripCrewOrchestrator
import json

def run_local_test():
    print("🚀 Initializing TripMind AI Orchestrator...")
    orchestrator = TripCrewOrchestrator()

    # Mock frontend JSON payload based on the Figma spec demo
    mock_frontend_input = {
        "destination": "Goa, India",
        "startDate": "2026-06-15",
        "endDate": "2026-06-21",
        "kids": 1,
        "adults": 2,
        "seniors": 1,
        "budget": 140000,
        "budgetMode": "Premium",
        "foodPref": "Veg",
        "travelStyle": "Relaxed",
        "interests": ["Nature", "Food", "History"]
    }

    print(f"🌍 Planning trip to {mock_frontend_input['destination']}...")
    
    # Run the Crew
    final_trip_plan = orchestrator.plan_trip(mock_frontend_input)

    # Output the result beautifully
    print("\n✅ Trip Generation Complete! Final JSON Output:")
    print(json.dumps(final_trip_plan, indent=4))

if __name__ == "__main__":
    run_local_test()