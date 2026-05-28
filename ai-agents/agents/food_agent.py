from crewai import Agent
from config.llm_config import groq_llm
from tools.search_tools import SearchTools

class FoodAgent:
    def __init__(self):
        # Groq is the default provider for culinary recommendations and fast extraction.
        self.llm = groq_llm

    def create_agent(self) -> Agent:
        return Agent(
            role="Culinary & Dining Specialist",
            goal="Curate a list of restaurant and cafe recommendations that fit the group's dietary preferences and budget.",
            backstory=(
                "You are a local food critic and dietary expert. You search the internet "
                "to find highly-rated dining spots near the planned itinerary locations. "
                "You strictly filter based on the user's food preference (e.g., Veg, Non-Veg, Both) "
                "and budget. For every restaurant you recommend, you MUST include a short "
                "'Why this place' explanation and its cuisine type."
            ),
            tools=[SearchTools.search_internet],
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )