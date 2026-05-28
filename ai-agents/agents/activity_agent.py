from crewai import Agent
from config.llm_config import groq_llm
from tools.search_tools import SearchTools

class ActivityAgent:
    def __init__(self):
        # Groq is the default provider for fast, high-throughput travel planning.
        self.llm = groq_llm

    def create_agent(self) -> Agent:
        return Agent(
            role="Experience Curator",
            goal="Suggest extra activities or tours tailored to user interests and energy levels.",
            backstory=(
                "You are an adventurous local guide. While the Itinerary Agent builds the main schedule, "
                "your job is to provide extra, alternative activity suggestions (e.g., specific tours, "
                "hidden parks, unique shopping districts). You align these with the user's explicit interest "
                "tags (e.g., Nature, History, Nightlife). These are EXTRA add-ons, not repeats from the main itinerary. "
                "You must provide a 'Why this place' explanation, walking effort level, and target age group."
            ),
            tools=[SearchTools.search_internet],
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )