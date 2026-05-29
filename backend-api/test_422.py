import requests

payload = {
    "destination": "Tokyo, Japan",
    "start_date": "2026-06-01",
    "end_date": "2026-06-05",
    "travelers": {
        "kids": 0,
        "adults": 1,
        "seniors": 0
    },
    "budget_inr": 75000,
    "food_preference": "Any",
    "travel_style": "Balanced",
    "interests": ["Culture", "Food"]
}

try:
    response = requests.post("http://127.0.0.1:8000/api/v1/plan", json=payload)
    print(response.status_code)
    if response.status_code == 422:
        print(response.json())
except Exception as e:
    print(e)
