from crewai import Agent
from config.llm_config import groq_llm

class TravelerProfileAgent:
    def __init__(self):
        # Groq is the default provider for profile analysis and demographic summarization.
        self.llm = groq_llm

    def create_agent(self) -> Agent:
        return Agent(
            role="Expert Travel Profiler",
            goal="Analyze traveler demographics and preferences to create a precise, actionable group profile.",
            backstory=(
                "You are a behavioral psychology and travel logistics expert. "
                "Your job is to look at a group's composition (kids, adults, seniors), "
                "budget, and preferences to define their energy levels, walking capability, "
                "and ideal pacing. You ensure subsequent planning agents know exactly WHO they are planning for. "
                "You do not plan the itinerary; you only analyze the people."
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    