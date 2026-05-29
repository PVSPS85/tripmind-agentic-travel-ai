from tools.search_tools import SearchTools
from config.llm_config import groq_llm
from crewai import Agent
from tools.weather_tools import WeatherTools


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
            
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

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
            tools=[WeatherTools.get_weather],
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
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
            
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
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
             # Giving this agent the ability to Google search
            verbose=True,
            allow_delegation=False,
            # tools removed for speed)
            llm=self.llm
        )

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
            
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
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
    