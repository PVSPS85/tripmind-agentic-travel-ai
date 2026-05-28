import httpx
from typing import Dict, Any, List
from app.config import settings

class OpenWeatherToolWrapper:
    """
    Provides real-time climatic evaluation contexts enabling 
    itinerary adaptive structural overrides.
    """

    @staticmethod
    async def fetch_climatology_summary(destination: str) -> Dict[str, Any]:
        fallback_data = {
            "expected_condition": "Mild overcast clear indices with isolated standard precipitation gaps",
            "packing_suggestions": ["Comfortable walking shoes", "Breathable layers", "Compact umbrella protection packs"],
            "adaptive_itinerary_note": "Standard daytime itineraries require minimal environmental restructuring safeguards."
        }
        
        if not settings.OPENWEATHER_API_KEY:
            return fallback_data

        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {"q": destination, "appid": settings.OPENWEATHER_API_KEY, "units": "metric"}

        async with httpx.AsyncClient(timeout=4.0) as client:
            try:
                response = await client.get(url, params=params)
                if response.status_code == 200:
                    res_json = response.json()
                    weather_desc = res_json["weather"][0]["description"] if res_json.get("weather") else "Clear Sky"
                    
                    # Synthesize structural packing vectors intelligently based on simple metric bounds
                    temp = res_json.get("main", {}).get("temp", 25)
                    packing = ["Sunscreen lotion", "Sunglasses"] if temp > 28 else ["Light jacket layers"]
                    packing.append("Universal charging brick adapters")

                    return {
                        "expected_condition": f"Temperature around {temp}°C with {weather_desc}.",
                        "packing_suggestions": packing,
                        "adaptive_itinerary_note": "Outdoor conditions match generic traveler health profiles."
                    }
                return fallback_data
            except httpx.HTTPError:
                return fallback_data
