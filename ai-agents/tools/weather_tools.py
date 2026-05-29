import os
import requests
from crewai.tools import tool

class WeatherTools:
    @tool("Get weather forecast")
    def get_weather(city: str) -> str:
        """Useful to get the current and forecasted weather for a specific city. Input should be just the city name."""
        api_key = os.environ.get('OPENWEATHER_API_KEY')
        if not api_key:
            return "Weather API key not configured in environment."
            
        # Using metric units for Celsius to match the Figma design (e.g., "25°C")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            
            return f"The current weather in {city} is {temp}°C with {desc}."
            
        except requests.exceptions.RequestException as e:
            return f"Could not fetch weather data for {city}. Assume average seasonal weather. Error: {e}"
