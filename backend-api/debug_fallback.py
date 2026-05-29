import sys
import os
sys.path.append(os.path.abspath("../ai-agents"))
from crew_orchestrator import TripCrewOrchestrator

def test():
    orch = TripCrewOrchestrator()
    try:
        orch.plan_trip({
            "destination": "Tokyo, Japan",
            "start_date": "2026-06-01",
            "end_date": "2026-06-05",
            "kids": 0, "adults": 1, "seniors": 0,
            "startDate": "2026-06-01", "endDate": "2026-06-05",
            "budgetMode": "Moderate", "foodPref": "Any",
            "interests": ["Culture", "Food", "Technology"],
            "travelStyle": "Active"
        })
    except Exception as e:
        print(f"Exception type: {type(e)}")
        print(f"Exception string: {str(e)}")

test()
