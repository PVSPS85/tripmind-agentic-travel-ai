from crewai import Agent
from config.llm_config import groq_llm
from tools.search_tools import SearchTools
from tools.weather_tools import WeatherTools

class TransportAgent:
    def __init__(self):
        # Groq is the default provider; Gemini remains a fallback only when needed.
        self.llm = groq_llm

    def create_agent(self) -> Agent:
        return Agent(
            role="Logistics and Weather Adaptor",
            goal="Analyze the daily itinerary, calculate transit times, and adapt the schedule based on weather forecasts.",
            backstory=(
                "You are a master of logistics. You look at the day-by-day itinerary and "
                "figure out the best way to get from point A to point B (e.g., walk, cab, metro) "
                "along with estimated costs and times. Furthermore, you ALWAYS check the weather. "
                "If rain or extreme weather is forecasted, you act as a safety net: you dynamically "
                "swap heavy outdoor activities for indoor alternatives (like museums) and add a "
                "'Rain backup' note to the day."
            ),
            tools=[SearchTools.search_internet, WeatherTools.get_weather],
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )