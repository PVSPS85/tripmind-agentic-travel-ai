import json
import math
import re
import signal
import time
from crewai import Task, Crew, Process
from config.llm_config import gemini_llm, groq_llm
from agents.profile_agent import TravelerProfileAgent
from agents.destination_agent import DestinationAgent
from agents.itinerary_agent import ItineraryAgent
from agents.hotel_agent import HotelAgent
from agents.food_agent import FoodAgent
from agents.transport_agent import TransportAgent
from agents.activity_agent import ActivityAgent


def clean_json_output(raw_output):
    if isinstance(raw_output, (dict, list)):
        return raw_output

    text = str(raw_output).strip()
    if not text:
        return ""

    text = re.sub(r"```(?:json)?", "", text, flags=re.IGNORECASE)
    text = text.strip()
    return text


class TripCrewOrchestrator:
    def __init__(self):
        self.primary_llm = groq_llm
        self.fallback_llm = gemini_llm
        self._rebuild_agents(self.primary_llm)

    def _build_agent(self, agent_factory, llm):
        agent_wrapper = agent_factory()
        agent_wrapper.llm = llm
        return agent_wrapper.create_agent()

    def _rebuild_agents(self, llm):
        self.profile_agent = self._build_agent(TravelerProfileAgent, llm)
        self.destination_agent = self._build_agent(DestinationAgent, llm)
        self.itinerary_agent = self._build_agent(ItineraryAgent, llm)
        self.hotel_agent = self._build_agent(HotelAgent, llm)
        self.food_agent = self._build_agent(FoodAgent, llm)
        self.transport_agent = self._build_agent(TransportAgent, llm)
        self.activity_agent = self._build_agent(ActivityAgent, llm)

        self.all_agents = {
            "profile_agent": self.profile_agent,
            "destination_agent": self.destination_agent,
            "itinerary_agent": self.itinerary_agent,
            "hotel_agent": self.hotel_agent,
            "food_agent": self.food_agent,
            "transport_agent": self.transport_agent,
            "activity_agent": self.activity_agent,
        }

        self.fallback_agents = dict(self.all_agents)

    def _reset_default_llms(self):
        self._rebuild_agents(self.primary_llm)

    def _apply_fallback_llms(self):
        self._rebuild_agents(self.fallback_llm)

    def _extract_retry_after_seconds(self, error_message: str) -> float | None:
        lowered = str(error_message).lower()
        match = re.search(
            r"(?:try again in|please retry in)\s+([0-9]+(?:\.[0-9]+)?)\s*(?:s|sec|seconds)?",
            lowered,
        )
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
        return None

    def _calculate_retry_delay(self, error_message: str, attempt: int) -> float:
        retry_after_seconds = self._extract_retry_after_seconds(error_message)
        if retry_after_seconds is not None:
            return max(retry_after_seconds, 0.0)
        return min(8.0, 2 ** (attempt - 1))

    def _run_crew_with_timeout(self, trip_crew, execution_timeout: float):
        original_handler = signal.getsignal(signal.SIGALRM)

        def timeout_handler(_signum, _frame):
            raise TimeoutError(f"Crew execution timed out after {execution_timeout} seconds")

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(math.ceil(execution_timeout))
        try:
            return trip_crew.kickoff()
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, original_handler)

    def _execute_crew_with_retry(self, trip_crew, max_attempts: int = 2, execution_timeout: float = 20.0):
        last_error = None
        for attempt in range(1, max_attempts + 1):
            try:
                return self._run_crew_with_timeout(trip_crew, execution_timeout)
            except Exception as exc:
                last_error = exc
                error_message = str(exc)
                if attempt >= max_attempts or not self._should_retry_with_fallback(error_message):
                    raise
                delay = self._calculate_retry_delay(error_message, attempt)
                time.sleep(delay)

        if last_error is not None:
            raise last_error
        raise RuntimeError("Crew execution failed without a captured exception")

    def _should_retry_with_fallback(self, error_message: str) -> bool:
        lowered = str(error_message).lower()
        retry_markers = [
            "429",
            "resource_exhausted",
            "quota",
            "rate limit",
            "timed out",
            "timeout",
            "badrequest",
            "decommissioned",
            "unsupported",
        ]
        return any(marker in lowered for marker in retry_markers)

    def _extract_json_payload(self, raw_output):
        cleaned_output = clean_json_output(raw_output)

        if isinstance(cleaned_output, dict):
            return cleaned_output

        if isinstance(cleaned_output, list):
            return cleaned_output

        text = str(cleaned_output).strip()
        if not text:
            return None

        for start_index, char in enumerate(text):
            if char in "{[":
                candidate = text[start_index:].strip()
                try:
                    parsed, _ = json.JSONDecoder().raw_decode(candidate)
                    return parsed
                except json.JSONDecodeError:
                    continue

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None

    def _parse_result(self, raw_output):
        parsed = self._extract_json_payload(raw_output)
        if isinstance(parsed, dict):
            return parsed
        if isinstance(parsed, list):
            return {"items": parsed}
        return {
            "error": "Crew AI failed to return valid JSON",
            "raw_output": str(raw_output),
        }

    def _estimate_trip_days(self, trip_inputs: dict) -> int:
        start_date = trip_inputs.get("startDate")
        end_date = trip_inputs.get("endDate")
        try:
            from datetime import datetime

            start = datetime.fromisoformat(str(start_date)).date()
            end = datetime.fromisoformat(str(end_date)).date()
            delta_days = (end - start).days
            if delta_days > 0:
                return min(delta_days, 7)
        except (TypeError, ValueError):
            pass

        interests = trip_inputs.get("interests") or []
        return max(1, min(7, len(interests) or 3))

    def _build_offline_fallback_plan(self, trip_inputs: dict, provider_error: str) -> dict:
        trip_days = self._estimate_trip_days(trip_inputs)
        itinerary_days = []
        for day in range(1, trip_days + 1):
            itinerary_days.append({
                "day": day,
                "morning": "Start with a relaxed local breakfast and a scenic walk.",
                "afternoon": "Explore the main attraction cluster and local markets.",
                "evening": "Enjoy a comfortable dinner and a low-stress return to rest.",
            })

        destination = trip_inputs.get("destination", "your destination")
        budget_mode = trip_inputs.get("budgetMode", "standard")
        food_pref = trip_inputs.get("foodPref", "local cuisine")

        return {
            "status": "offline_fallback",
            "summary": f"Generated a local fallback itinerary for {destination} because the LLM providers are rate-limited.",
            "provider_error": provider_error,
            "trip_inputs": trip_inputs,
            "itinerary": {
                "destination": destination,
                "duration_days": trip_days,
                "days": itinerary_days,
            },
            "recommendations": {
                "hotels": [
                    {
                        "name": f"Central stay in {destination}",
                        "budget_mode": budget_mode,
                        "reason": "Reliable location with easy access to attractions.",
                    }
                ],
                "food": [
                    {
                        "name": f"Vegetarian-friendly local spot",
                        "preference": food_pref,
                        "reason": "Works well for relaxed dining and local flavors.",
                    }
                ],
                "activities": [
                    {
                        "name": "Scenic attraction visit",
                        "reason": "Fits a relaxed travel style and low-friction pacing.",
                    }
                ],
            },
            "transport": {
                "arrival": "Use an airport transfer, taxi, or local transit based on arrival point.",
                "local_mobility": "Keep one light transit option and one backup option for each day.",
            },
            "fallback_note": "This is a locally generated fallback because external AI providers exceeded quota or rate limits.",
        }

    def _build_trip_crew(self, trip_inputs: dict) -> Crew:
        # 1. Profile Task
        profile_task = Task(
            description=f"Analyze the following travelers: {trip_inputs['kids']} kids, {trip_inputs['adults']} adults, {trip_inputs['seniors']} seniors. Travel style is {trip_inputs['travelStyle']}.",
            expected_output="A brief JSON summary of the group's demographics, energy levels, and walking capability.",
            agent=self.profile_agent
        )

        # 2. Destination Task
        destination_task = Task(
            description=f"Research {trip_inputs['destination']} for a trip in the month of {trip_inputs['startDate']}.",
            expected_output="A JSON list of the top 5-7 attractions, seasonal weather context, and peak tourist traps to avoid.",
            agent=self.destination_agent
        )

        # 3. Core Itinerary Task (Depends on Profile & Destination)
        itinerary_task = Task(
            description=f"Draft a day-by-day schedule from {trip_inputs['startDate']} to {trip_inputs['endDate']} for {trip_inputs['destination']}.",
            expected_output="A structured JSON day-by-day skeleton with morning, afternoon, and evening slots.",
            agent=self.itinerary_agent,
            context=[profile_task, destination_task]
        )

        # 4. Recommendation Tasks (Can run independently based on user inputs)
        hotel_task = Task(
            description=f"Find hotels in {trip_inputs['destination']} matching a {trip_inputs['budgetMode']} budget.",
            expected_output="JSON list of 3-5 hotels with name, rating, price estimate, and a 'Why this place' reason.",
            agent=self.hotel_agent,
            context=[profile_task]
        )

        food_task = Task(
            description=f"Find {trip_inputs['foodPref']} restaurants in {trip_inputs['destination']} fitting a {trip_inputs['budgetMode']} budget.",
            expected_output="JSON list of restaurants with cuisine type, Veg/Non-Veg status, and a 'Why this place' reason.",
            agent=self.food_agent
        )

        activity_task = Task(
            description=f"Find extra activities in {trip_inputs['destination']} matching these interests: {', '.join(trip_inputs['interests'])}.",
            expected_output="JSON list of extra activities, not repeating the main itinerary, with a target age group and walking effort.",
            agent=self.activity_agent
        )

        # 5. Final Polish Task (Transport & Weather integration)
        transport_task = Task(
            description=f"Review the drafted itinerary for {trip_inputs['destination']} and calculate transit modes. Check the weather.",
            expected_output="The final, combined JSON dashboard payload including the itinerary with transit chips, weather backups, hotels, food, and activities.",
            agent=self.transport_agent,
            context=[itinerary_task, hotel_task, food_task, activity_task]
        )

        return Crew(
            agents=[
                self.profile_agent, self.destination_agent, self.itinerary_agent,
                self.hotel_agent, self.food_agent, self.activity_agent, self.transport_agent
            ],
            tasks=[
                profile_task, destination_task, itinerary_task,
                hotel_task, food_task, activity_task, transport_task
            ],
            process=Process.sequential,
            verbose=True
        )

    def plan_trip(self, trip_inputs: dict) -> dict:
        """
        Takes the raw JSON input from the frontend and orchestrates the multi-agent workflow.
        """
        self._reset_default_llms()
        trip_crew = self._build_trip_crew(trip_inputs)

        try:
            raw_result = self._execute_crew_with_retry(trip_crew)
            cleaned_result = clean_json_output(raw_result)
            return self._parse_result(cleaned_result)
        except Exception as exc:
            if self._should_retry_with_fallback(str(exc)):
                self._apply_fallback_llms()
                trip_crew = self._build_trip_crew(trip_inputs)
                try:
                    raw_result = self._execute_crew_with_retry(trip_crew)
                    cleaned_result = clean_json_output(raw_result)
                    return self._parse_result(cleaned_result)
                except Exception as fallback_exc:
                    return self._build_offline_fallback_plan(
                        trip_inputs,
                        str(fallback_exc),
                    )

            return {
                "error": "Crew execution failed",
                "details": str(exc),
            }
