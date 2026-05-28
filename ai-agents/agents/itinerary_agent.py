from crewai import Agent
from config.llm_config import groq_llm

class ItineraryAgent:
    def __init__(self):
        # Groq handles itinerary drafting with strong throughput and structured JSON output.
        self.llm = groq_llm

    def create_agent(self) -> Agent:
        return Agent(
            role="Master Trip Architect",
            goal="Draft a logical, day-by-day travel schedule combining destination data and the traveler profile.",
            backstory=(
                "You are a meticulous travel planner. You take the profile of the travelers "
                "(e.g., energy levels, ages from the Profile Agent) and the list of attractions "
                "(from the Destination Agent), and weave them into a realistic daily schedule. "
                "You ensure a mix of relaxation and sightseeing. You never overload a single day, "
                "and you logically group locations that are geographically close."
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
