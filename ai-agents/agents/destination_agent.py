from crewai import Agent
from config.llm_config import groq_llm
from tools.search_tools import SearchTools

class DestinationAgent:
    def __init__(self):
        # We use Groq (Llama 3) here because it is incredibly fast at reading 
        # search results and extracting key data points without latency.
        self.llm = groq_llm

    def create_agent(self) -> Agent:
        return Agent(
            role="Local Destination Expert",
            goal="Discover top attractions, cultural highlights, and practical travel context for the given destination.",
            backstory=(
                "You are a seasoned local guide. You know the best places to visit, "
                "the peak seasons, and hidden gems. Your job is to search the internet "
                "to gather raw, up-to-date data about the city so the Itinerary Agent "
                "has real, exciting places to schedule."
            ),
            tools=[SearchTools.search_internet], # Giving this agent the ability to Google search
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
