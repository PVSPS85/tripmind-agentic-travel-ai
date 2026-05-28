from crewai import Agent
from config.llm_config import groq_llm
from tools.search_tools import SearchTools

class HotelAgent:
    def __init__(self):
        self.llm = groq_llm

    def create_agent(self) -> Agent:
        return Agent(
            role="Accommodation Specialist",
            goal="Recommend 3 to 5 hotels that perfectly match the group's budget, style, and demographic.",
            backstory=(
                "You are a luxury concierge and budget-savvy travel agent combined. "
                "You search the internet for real, highly-rated hotels in the destination city. "
                "You ensure the recommendations strictly align with the user's budget mode "
                "(e.g., Budget, Premium) and traveler tags (e.g., Family-friendly). "
                "You must provide a short 'Why this place' reason for every hotel you recommend."
            ),
            tools=[SearchTools.search_internet],
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
