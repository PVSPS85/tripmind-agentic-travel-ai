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
from mock_data_ooty import get_ooty_mock


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
        # The signal module only works in the main thread.
        # Since we use asyncio.to_thread, we cannot use signal.alarm.
        # We'll just let CrewAI run.
        return trip_crew.kickoff()

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
        dest = trip_inputs.get("destination", "Goa").strip()
        dest_lower = dest.lower()

        if "bengaluru" in dest_lower or "bangalore" in dest_lower:
            return self._build_bengaluru_mock(trip_days, dest, provider_error)
        elif "ooty" in dest_lower:
            return get_ooty_mock(trip_days, dest, provider_error)
        elif "goa" in dest_lower:
            return self._build_goa_mock(trip_days, dest, provider_error)
        else:
            return self._build_goa_mock(trip_days, dest, provider_error) # Default to Goa-style richness

    def _build_bengaluru_mock(self, trip_days, dest, provider_error) -> dict:
        itinerary_days = []
        for day in range(1, trip_days + 1):
            itinerary_days.append({
                "day_number": day,
                "date_string": f"Day {day}",
                "theme": "Tech & Heritage" if day % 2 == 1 else "Gardens & Gastronomy",
                "day_energy_badge": "Balanced",
                "weather_forecast": "Pleasant 24°C",
                "activities": [
                    {
                        "time_slot": "Morning",
                        "start_time": "08:30",
                        "activity_name": "Cubbon Park Walk & Breakfast at MTR",
                        "description": "Start the day with a refreshing walk in the lungs of the city followed by legendary filter coffee.",
                        "estimated_cost_inr": 350.0,
                        "target_age_group": "Families",
                        "walking_effort": "Moderate walk",
                        "energy_level": "Active",
                        "transit_estimate": "🚗 15 min • ₹120",
                        "image_url": "https://images.unsplash.com/photo-1593693397690-362bcbc72c3d?w=800&q=80",
                        "explainability": {"reason_why": "Iconic Bengaluru morning experience. Great for all ages.", "best_time_to_visit": "08:30 AM"}
                    },
                    {
                        "time_slot": "Afternoon",
                        "start_time": "13:30",
                        "activity_name": "Visvesvaraya Industrial & Technological Museum",
                        "description": "Interactive science exhibits perfect for kids and curious minds.",
                        "estimated_cost_inr": 500.0,
                        "target_age_group": "Kids & Teens",
                        "walking_effort": "Moderate walk",
                        "energy_level": "Balanced",
                        "transit_estimate": "🚶 10 min • Free",
                        "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80",
                        "explainability": {"reason_why": "Indoor activity to escape the afternoon sun, highly engaging.", "best_time_to_visit": "02:00 PM"}
                    },
                    {
                        "time_slot": "Evening",
                        "start_time": "18:00",
                        "activity_name": "Brewery Hopping in Indiranagar",
                        "description": "Experience India's pub capital with craft beers and global tapas.",
                        "estimated_cost_inr": 2500.0,
                        "target_age_group": "Adults",
                        "walking_effort": "Low walk",
                        "energy_level": "Relaxed",
                        "transit_estimate": "🚗 25 min • ₹250",
                        "image_url": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800&q=80",
                        "explainability": {"reason_why": "Bengaluru is famous for its microbreweries.", "best_time_to_visit": "07:00 PM"}
                    }
                ]
            })

        return {
            "destination": dest,
            "duration_days": trip_days,
            "ai_optimization_summary": ["Optimized for Bengaluru traffic patterns.", "Included heritage and tech fusion."],
            "weather_pipeline": {
                "expected_condition": "Pleasant • 22-28°C",
                "packing_suggestions": ["Light jacket", "Comfortable walking shoes", "Umbrella"],
                "adaptive_itinerary_note": "Bangalore weather can change rapidly; keep an umbrella handy for sudden evening showers."
            },
            "budget_intelligence": {
                "allocated_hotels_total_inr": 18000.0, "allocated_food_total_inr": 12000.0,
                "allocated_activities_total_inr": 8000.0, "allocated_transport_total_inr": 4000.0,
                "remaining_buffer_inr": 5000.0, "summary_insight": "Balanced urban budget."
            },
            "hotels": [
                {
                    "name": "The Leela Palace Bengaluru",
                    "rating": 4.8, "price_per_night_inr": 16500.0, "location_area": "Indiranagar",
                    "image_url": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800&q=80",
                    "amenities_tags": ["Pool", "Spa", "Luxury"], "badges": ["Premium", "Couples"],
                    "explainability": {"reason_why": "Luxurious stay with magnificent architecture.", "best_time_to_visit": None}
                },
                {
                    "name": "Taj West End",
                    "rating": 4.7, "price_per_night_inr": 14000.0, "location_area": "Race Course Road",
                    "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",
                    "amenities_tags": ["Heritage", "Gardens"], "badges": ["Heritage", "Quiet"],
                    "explainability": {"reason_why": "A tranquil oasis in the middle of the bustling city.", "best_time_to_visit": None}
                },
                {
                    "name": "Lemon Tree Premier",
                    "rating": 4.3, "price_per_night_inr": 6500.0, "location_area": "Ulsoor Lake",
                    "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
                    "amenities_tags": ["Breakfast", "WiFi", "Gym"], "badges": ["Budget", "Business"],
                    "explainability": {"reason_why": "Great value, central location near the lake.", "best_time_to_visit": None}
                }
            ],
            "food_and_dining": [
                {
                    "restaurant_name": "Toit Brewpub",
                    "cuisine_type": "Pub Food • Craft Beer",
                    "rating": 4.7, "dietary_suitability": "Both", "estimated_cost_per_person_inr": 1500.0,
                    "distance": "Indiranagar • 4 km", "image_url": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800&q=80",
                    "explainability": {"reason_why": "The quintessential Bangalore brewery experience.", "best_time_to_visit": None}
                },
                {
                    "restaurant_name": "MTR (Mavalli Tiffin Room)",
                    "cuisine_type": "South Indian Veg",
                    "rating": 4.6, "dietary_suitability": "Veg", "estimated_cost_per_person_inr": 350.0,
                    "distance": "Lalbagh • 6 km", "image_url": "https://images.unsplash.com/photo-1589301760014-d929f39ce9b1?w=800&q=80",
                    "explainability": {"reason_why": "Historic establishment for authentic local breakfast.", "best_time_to_visit": None}
                },
                {
                    "restaurant_name": "Rameshwaram Cafe",
                    "cuisine_type": "South Indian Quick Bites",
                    "rating": 4.5, "dietary_suitability": "Veg", "estimated_cost_per_person_inr": 250.0,
                    "distance": "Indiranagar • 3.5 km", "image_url": "https://images.unsplash.com/photo-1610192244261-3f33de3f55e4?w=800&q=80",
                    "explainability": {"reason_why": "Viral local hotspot for the best ghee podi idlis.", "best_time_to_visit": None}
                }
            ],
            "extra_activities": [
                {
                    "activity_name": "Sunrise at Nandi Hills", "image_url": "https://images.unsplash.com/photo-1593693397690-362bcbc72c3d?w=800&q=80",
                    "rating": 4.6, "category": "Nature • Viewpoint", "target_age_group": "Adults",
                    "walking_effort": "Moderate walk", "energy_level": "Active", "duration": "4 hrs", "best_time": "05:00 AM",
                    "tags": ["Nature", "Outdoors", "Early Morning"],
                    "explainability": {"reason_why": "Classic Bangalore weekend drive above the clouds.", "best_time_to_visit": "05:30 AM"}
                },
                {
                    "activity_name": "Bangalore Palace Tour", "image_url": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=800&q=80",
                    "rating": 4.4, "category": "Heritage", "target_age_group": "Families",
                    "walking_effort": "Low walk", "energy_level": "Relaxed", "duration": "2 hrs", "best_time": "Afternoon",
                    "tags": ["Heritage", "Photography", "Indoor"],
                    "explainability": {"reason_why": "Tudor-style architecture right in the city center.", "best_time_to_visit": "03:00 PM"}
                }
            ],
            "transportation": [
                {"mode": "Namma Metro", "duration": "Varies", "cost_estimate": "₹30-₹60 per trip", "badges": ["Beat Traffic", "Budget"], "explainability": {"reason_why": "Fastest way to bypass Bangalore's notorious traffic.", "best_time_to_visit": None}},
                {"mode": "Uber / Ola Auto", "duration": "10-25 mins", "cost_estimate": "₹80-₹200", "badges": ["Last Mile", "Local Vibe"], "explainability": {"reason_why": "Ideal for short distances within neighborhoods.", "best_time_to_visit": None}}
            ],
            "itinerary": itinerary_days
        }

    def _build_goa_mock(self, trip_days, dest, provider_error) -> dict:
        itinerary_days = []
        for day in range(1, trip_days + 1):
            itinerary_days.append({
                "day_number": day,
                "date_string": f"Day {day}",
                "theme": "Beaches & Sunsets" if day % 2 == 1 else "Heritage & Spices",
                "day_energy_badge": "Relaxed",
                "weather_forecast": "Sunny 31°C",
                "activities": [
                    {
                        "time_slot": "Morning",
                        "start_time": "09:30",
                        "activity_name": "Fontainhas Latin Quarter Walk",
                        "description": "Explore the colorful Portuguese heritage streets and grab a local pastry.",
                        "estimated_cost_inr": 300.0,
                        "target_age_group": "Families",
                        "walking_effort": "Moderate walk",
                        "energy_level": "Balanced",
                        "transit_estimate": "🚗 20 min • ₹300",
                        "image_url": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800&q=80",
                        "explainability": {"reason_why": "Best done in the morning before it gets too hot.", "best_time_to_visit": "09:00 AM"}
                    },
                    {
                        "time_slot": "Afternoon",
                        "start_time": "13:30",
                        "activity_name": "Seafood Lunch at Martin's Corner",
                        "description": "Legendary Goan seafood in a relaxed, family-friendly setting.",
                        "estimated_cost_inr": 1200.0,
                        "target_age_group": "All Ages",
                        "walking_effort": "Low walk",
                        "energy_level": "Relaxed",
                        "transit_estimate": "🚗 30 min • ₹500",
                        "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80",
                        "explainability": {"reason_why": "A staple of South Goan culinary culture.", "best_time_to_visit": "01:30 PM"}
                    },
                    {
                        "time_slot": "Evening",
                        "start_time": "17:30",
                        "activity_name": "Sunset Beach Shack",
                        "description": "Relax on a sunbed with a mocktail while watching the waves.",
                        "estimated_cost_inr": 800.0,
                        "target_age_group": "Adults & Teens",
                        "walking_effort": "Low walk",
                        "energy_level": "Relaxed",
                        "transit_estimate": "🚶 5 min • Free",
                        "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",
                        "explainability": {"reason_why": "The perfect way to wind down a day in Goa.", "best_time_to_visit": "Sunset"}
                    }
                ]
            })

        return {
            "destination": dest,
            "duration_days": trip_days,
            "ai_optimization_summary": ["Curated a premium coastal itinerary.", "Balanced beach time with heritage."],
            "weather_pipeline": {
                "expected_condition": "Tropical • 28-32°C",
                "packing_suggestions": ["Light cottons", "Sunscreen", "Mosquito repellent"],
                "adaptive_itinerary_note": "Ensure you stay hydrated and seek shade during peak afternoon hours."
            },
            "budget_intelligence": {
                "allocated_hotels_total_inr": 25000.0, "allocated_food_total_inr": 18000.0,
                "allocated_activities_total_inr": 12000.0, "allocated_transport_total_inr": 6000.0,
                "remaining_buffer_inr": 8000.0, "summary_insight": "Premium beach holiday budget."
            },
            "hotels": [
                {
                    "name": "Taj Exotica Resort & Spa",
                    "rating": 4.9, "price_per_night_inr": 22000.0, "location_area": "Benaulim",
                    "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",
                    "amenities_tags": ["Private Beach", "Luxury Spa", "Kids Club"], "badges": ["Ultra Luxury", "Family-friendly", "Beachfront"],
                    "explainability": {"reason_why": "Sprawling luxury property with direct, clean beach access.", "best_time_to_visit": None}
                },
                {
                    "name": "W Goa",
                    "rating": 4.7, "price_per_night_inr": 18500.0, "location_area": "Vagator",
                    "image_url": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800&q=80",
                    "amenities_tags": ["Party Vibe", "Clifftop Pool"], "badges": ["Premium", "Couples", "Nightlife"],
                    "explainability": {"reason_why": "High energy, stunning sunset views from the rock pool.", "best_time_to_visit": None}
                },
                {
                    "name": "Fairfield by Marriott",
                    "rating": 4.4, "price_per_night_inr": 8500.0, "location_area": "Benaulim",
                    "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",
                    "amenities_tags": ["Pool", "Breakfast"], "badges": ["Value", "Quiet"],
                    "explainability": {"reason_why": "Reliable Marriott quality at a sensible price point.", "best_time_to_visit": None}
                },
                {
                    "name": "Azaya Beach Resort",
                    "rating": 4.6, "price_per_night_inr": 14000.0, "location_area": "Benaulim",
                    "image_url": "https://images.unsplash.com/photo-1499793983690-e29da59ef1c2?w=800&q=80",
                    "amenities_tags": ["Boutique", "Beach Access"], "badges": ["Trendy", "Couples"],
                    "explainability": {"reason_why": "Maldives-style villas right on the pristine white sands.", "best_time_to_visit": None}
                }
            ],
            "food_and_dining": [
                {
                    "restaurant_name": "Thalassa",
                    "cuisine_type": "Greek • Mediterranean",
                    "rating": 4.6, "dietary_suitability": "Both", "estimated_cost_per_person_inr": 1800.0,
                    "distance": "Siolim • 8 km", "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&q=80",
                    "explainability": {"reason_why": "Iconic sunset dining with plate-smashing entertainment.", "best_time_to_visit": None}
                },
                {
                    "restaurant_name": "Vinayak Family Restaurant",
                    "cuisine_type": "Authentic Goan Thali",
                    "rating": 4.7, "dietary_suitability": "Non-Veg", "estimated_cost_per_person_inr": 400.0,
                    "distance": "Assagao • 5 km", "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&q=80",
                    "explainability": {"reason_why": "Where the locals eat. The fish thali is unmatched.", "best_time_to_visit": None}
                },
                {
                    "restaurant_name": "Gunpowder",
                    "cuisine_type": "South Indian Coastal",
                    "rating": 4.8, "dietary_suitability": "Both", "estimated_cost_per_person_inr": 1500.0,
                    "distance": "Assagao • 6 km", "image_url": "https://images.unsplash.com/photo-1589301760014-d929f39ce9b1?w=800&q=80",
                    "explainability": {"reason_why": "Boutique dining under trees with phenomenal curries.", "best_time_to_visit": None}
                }
            ],
            "extra_activities": [
                {
                    "activity_name": "Dudhsagar Waterfall Trek", "image_url": "https://images.unsplash.com/photo-1621644788320-b386ee35a125?w=800&q=80",
                    "rating": 4.7, "category": "Adventure", "target_age_group": "Adults & Teens",
                    "walking_effort": "High walk", "energy_level": "High Energy", "duration": "6 hrs", "best_time": "Morning",
                    "tags": ["Nature", "Trekking", "Adventure"],
                    "explainability": {"reason_why": "Spectacular 4-tiered waterfall deep in the jungle.", "best_time_to_visit": "07:00 AM"}
                },
                {
                    "activity_name": "Spice Plantation Tour", "image_url": "https://images.unsplash.com/photo-1549471013-3364d7220b75?w=800&q=80",
                    "rating": 4.5, "category": "Culture • Nature", "target_age_group": "Families & Seniors",
                    "walking_effort": "Low walk", "energy_level": "Relaxed", "duration": "3 hrs", "best_time": "Afternoon",
                    "tags": ["Family-friendly", "Educational", "Senior-friendly"],
                    "explainability": {"reason_why": "Shaded canopy walk learning about organic spices, with an authentic Goan lunch included.", "best_time_to_visit": "12:00 PM"}
                }
            ],
            "transportation": [
                {"mode": "Pre-booked AC SUV", "duration": "Full Day", "cost_estimate": "₹3,500/day", "badges": ["Family Comfort", "AC"], "explainability": {"reason_why": "Essential for families covering large distances in Goa.", "best_time_to_visit": None}},
                {"mode": "Scooter Rental (Activa)", "duration": "Per Day", "cost_estimate": "₹400-₹600/day", "badges": ["Couples", "Budget", "Freedom"], "explainability": {"reason_why": "The classic, cheapest, and most fun way to explore narrow coastal roads.", "best_time_to_visit": None}}
            ],
            "itinerary": itinerary_days
        }

    def _build_trip_crew(self, trip_inputs: dict) -> Crew:
        # 1. Profile Task
        profile_task = Task(
            description=f"Analyze the following travelers: {trip_inputs['kids']} kids, {trip_inputs['adults']} adults, {trip_inputs['seniors']} seniors. Travel style is {trip_inputs['travelStyle']}.",
            expected_output="A brief JSON summary of the group's demographics, energy levels, walking capability, and required accommodations (e.g. step-free access).",
            agent=self.profile_agent
        )

        # 2. Destination Task
        destination_task = Task(
            description=f"Research {trip_inputs['destination']} for a trip in the month of {trip_inputs['startDate']}.",
            expected_output="A JSON list of the top attractions, seasonal weather context, and peak tourist traps to avoid.",
            agent=self.destination_agent
        )

        # 3. Core Itinerary Task (Depends on Profile & Destination)
        itinerary_task = Task(
            description=f"Draft a day-by-day schedule from {trip_inputs['startDate']} to {trip_inputs['endDate']} for {trip_inputs['destination']}. YOU MUST assign specific `start_time` (e.g. '14:00'), `target_age_group` (e.g. 'Families'), `walking_effort` (e.g. 'Low walk'), `energy_level` (e.g. 'Relaxed'), and `transit_estimate` (e.g. '🚗 15 min • ₹250') for EVERY activity. Also assign a `day_energy_badge` ('Relaxed', 'Balanced', 'Active') and `weather_forecast` (e.g. 'Sunny 31°C') to each day. Supply dummy Unsplash image URLs for `image_url`.",
            expected_output="A structured JSON day-by-day skeleton with all requested rich metadata tags.",
            agent=self.itinerary_agent,
            context=[profile_task, destination_task]
        )

        # 4. Recommendation Tasks
        hotel_task = Task(
            description=f"Find hotels in {trip_inputs['destination']} matching a {trip_inputs['budgetMode']} budget.",
            expected_output="JSON list of 3-5 hotels with name, rating, price estimate, location_area, a dummy `image_url`, `amenities_tags`, specific `badges` (e.g. ['Family-friendly', 'Budget']), and a 'Why this place' reason.",
            agent=self.hotel_agent,
            context=[profile_task]
        )

        food_task = Task(
            description=f"Find {trip_inputs['foodPref']} restaurants in {trip_inputs['destination']} fitting a {trip_inputs['budgetMode']} budget.",
            expected_output="JSON list of restaurants with cuisine type, Veg/Non-Veg status, dummy `image_url`, physical `distance` estimate, and a 'Why this place' reason.",
            agent=self.food_agent
        )

        activity_task = Task(
            description=f"Find 4-6 EXTRA activities (hidden gems, rainy day backups) in {trip_inputs['destination']} matching interests: {', '.join(trip_inputs['interests'])}. DO NOT repeat the main itinerary.",
            expected_output="JSON list of `extra_activities` containing activity_name, dummy `image_url`, rating, category, target_age_group, walking_effort, energy_level, duration, best_time, tags, and explainability.",
            agent=self.activity_agent
        )

        # 5. Final Polish Task (Transport & Weather integration)
        transport_task = Task(
            description=f"Review the drafted itinerary for {trip_inputs['destination']}. Generate a `transportation` list with 2-4 overall transport modes (e.g., 'Pre-booked AC cab', 'Auto rickshaw') detailing `duration`, `cost_estimate`, and `badges`.",
            expected_output="The final, combined JSON dashboard payload strictly matching the `TripDashboardSchema` (including itinerary, hotels, food, transportation, extra_activities, weather, budget).",
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
            max_rpm=15,
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
            parsed = self._parse_result(cleaned_result)
            
            if isinstance(parsed, dict) and "itinerary" not in parsed:
                try:
                    itin_raw = trip_crew.tasks[2].output.raw
                    itin_parsed = self._extract_json_payload(itin_raw)
                    if isinstance(itin_parsed, dict) and "itinerary" in itin_parsed:
                        parsed["itinerary"] = itin_parsed["itinerary"]
                    elif isinstance(itin_parsed, list):
                        parsed["itinerary"] = itin_parsed
                    else:
                        parsed["itinerary"] = []
                except Exception:
                    parsed["itinerary"] = []
            return parsed
        except Exception as exc:
            if self._should_retry_with_fallback(str(exc)):
                self._apply_fallback_llms()
                trip_crew = self._build_trip_crew(trip_inputs)
                try:
                    raw_result = self._execute_crew_with_retry(trip_crew)
                    cleaned_result = clean_json_output(raw_result)
                    parsed = self._parse_result(cleaned_result)
                    
                    if isinstance(parsed, dict) and "itinerary" not in parsed:
                        try:
                            itin_raw = trip_crew.tasks[2].output.raw
                            itin_parsed = self._extract_json_payload(itin_raw)
                            if isinstance(itin_parsed, dict) and "itinerary" in itin_parsed:
                                parsed["itinerary"] = itin_parsed["itinerary"]
                            elif isinstance(itin_parsed, list):
                                parsed["itinerary"] = itin_parsed
                            else:
                                parsed["itinerary"] = []
                        except Exception:
                            parsed["itinerary"] = []
                    return parsed
                except Exception as fallback_exc:
                    return self._build_offline_fallback_plan(
                        trip_inputs,
                        str(fallback_exc),
                    )

            return self._build_offline_fallback_plan(
                trip_inputs,
                str(exc),
            )
