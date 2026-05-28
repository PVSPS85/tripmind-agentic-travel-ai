import httpx
from typing import Dict, Any, List
from app.config import settings

class SerperSearchToolWrapper:
    """
    Custom high-speed exploration tool wrapper mapping directly into 
    Google SERP data layers for real-world spot discoveries.
    """
    
    @staticmethod
    async def search_live_data(query: str, limit: int = 5) -> List[Dict[str, Any]]:
        if not settings.SERPER_API_KEY:
            # Fallback mock configuration allowing validation context layers during sandbox run loops
            return [{"title": f"Mock Spot for {query}", "snippet": "High quality real spot description context lines."}]

        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": settings.SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {"q": query, "num": limit}

        async with httpx.AsyncClient(timeout=6.0) as client:
            try:
                response = await client.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    return data.get("organic", [])
                return []
            except httpx.HTTPError:
                return []
