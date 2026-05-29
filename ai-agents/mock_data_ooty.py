def get_ooty_mock(trip_days: int, dest: str, provider_error: str) -> dict:
    itinerary_days = []
    for day in range(1, trip_days + 1):
        itinerary_days.append({
            "day_number": day,
            "date_string": f"Day {day}",
            "theme": "Lakes & Gardens" if day % 2 == 1 else "Tea Estates & Viewpoints",
            "day_energy_badge": "Relaxed",
            "weather_forecast": "Cool 18°C",
            "activities": [
                {
                    "time_slot": "Morning",
                    "start_time": "09:00",
                    "activity_name": "Boating at Ooty Lake",
                    "description": "Enjoy a peaceful morning paddleboat ride surrounded by eucalyptus trees.",
                    "estimated_cost_inr": 250.0,
                    "target_age_group": "Families",
                    "walking_effort": "Low walk",
                    "energy_level": "Relaxed",
                    "transit_estimate": "🚗 10 min • ₹150",
                    "image_url": "https://images.unsplash.com/photo-1596414545934-2e9ba40d1dfa?w=800&q=80",
                    "explainability": {"reason_why": "Iconic Ooty experience best done before the crowds arrive.", "best_time_to_visit": "09:00 AM"}
                },
                {
                    "time_slot": "Afternoon",
                    "start_time": "13:30",
                    "activity_name": "Government Botanical Garden",
                    "description": "Stroll through terraced gardens showcasing thousands of exotic plant species.",
                    "estimated_cost_inr": 100.0,
                    "target_age_group": "All Ages",
                    "walking_effort": "High walk",
                    "energy_level": "Balanced",
                    "transit_estimate": "🚶 15 min • Free",
                    "image_url": "https://images.unsplash.com/photo-1582200877983-097ea143a25b?w=800&q=80",
                    "explainability": {"reason_why": "A heritage garden dating back to 1848, perfect for a sunny afternoon.", "best_time_to_visit": "02:00 PM"}
                },
                {
                    "time_slot": "Evening",
                    "start_time": "17:00",
                    "activity_name": "Homemade Chocolates & Tea at Charing Cross",
                    "description": "Sample Ooty's famous local chocolates and warm Nilgiri tea.",
                    "estimated_cost_inr": 400.0,
                    "target_age_group": "Everyone",
                    "walking_effort": "Low walk",
                    "energy_level": "Relaxed",
                    "transit_estimate": "🚗 5 min • ₹100",
                    "image_url": "https://images.unsplash.com/photo-1620012253295-c15cb3e71240?w=800&q=80",
                    "explainability": {"reason_why": "Ooty is renowned for its locally crafted chocolates.", "best_time_to_visit": "05:30 PM"}
                }
            ]
        })

    return {
        "itinerary": itinerary_days,
        "destination": dest,
        "duration_days": trip_days,
        "ai_optimization_summary": ["Optimized for a serene hill station experience.", "Balanced sightseeing with relaxation."],
        "weather_pipeline": {
            "expected_condition": "Pleasant/Chilly • 15-22°C",
            "packing_suggestions": ["Warm jacket", "Comfortable walking shoes", "Umbrella"],
            "adaptive_itinerary_note": "Temperatures drop significantly in the evening; layer up."
        },
        "budget_intelligence": {
            "allocated_hotels_total_inr": 15000.0, "allocated_food_total_inr": 9000.0,
            "allocated_activities_total_inr": 4000.0, "allocated_transport_total_inr": 3000.0,
            "remaining_buffer_inr": 4000.0, "summary_insight": "Value hill-station budget."
        },
        "hotels": [
            {
                "name": "Savoy - IHCL SeleQtions",
                "rating": 4.8, "price_per_night_inr": 12500.0, "location_area": "Sylks Road",
                "image_url": "https://images.unsplash.com/photo-1542314831-c6a4d14d837e?w=800&q=80",
                "amenities_tags": ["Heritage", "Fireplace", "Spa"], "badges": ["Premium", "Couples"],
                "explainability": {"reason_why": "Historic 19th-century hotel offering old-world colonial charm.", "best_time_to_visit": None}
            },
            {
                "name": "Sterling Ooty Fern Hill",
                "rating": 4.4, "price_per_night_inr": 6500.0, "location_area": "Fern Hill",
                "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",
                "amenities_tags": ["Valley View", "Kids Play Area"], "badges": ["Family-friendly", "Value"],
                "explainability": {"reason_why": "Great views and family activities at a reasonable price point.", "best_time_to_visit": None}
            }
        ],
        "food_and_dining": [
            {
                "restaurant_name": "Earl's Secret",
                "cuisine_type": "Continental • Indian",
                "rating": 4.6, "dietary_suitability": "Both", "estimated_cost_per_person_inr": 800.0,
                "distance": "King's Cliff • 2 km", "image_url": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800&q=80",
                "explainability": {"reason_why": "Set in a restored British mansion, perfect for a classy dinner.", "best_time_to_visit": None}
            },
            {
                "restaurant_name": "Shinkows Chinese Restaurant",
                "cuisine_type": "Authentic Chinese",
                "rating": 4.5, "dietary_suitability": "Both", "estimated_cost_per_person_inr": 500.0,
                "distance": "Commissioner's Road • 1.5 km", "image_url": "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=800&q=80",
                "explainability": {"reason_why": "A legendary old-school eatery known for its signature chilly beef.", "best_time_to_visit": None}
            }
        ],
        "extra_activities": [
            {
                "activity_name": "Nilgiri Mountain Railway (Toy Train)", "image_url": "https://images.unsplash.com/photo-1535492193566-b333642730fb?w=800&q=80",
                "rating": 4.9, "category": "Heritage • Scenic", "target_age_group": "Families",
                "walking_effort": "Low walk", "energy_level": "Relaxed", "duration": "3 hrs", "best_time": "Morning",
                "tags": ["UNESCO", "Photography", "Train"],
                "explainability": {"reason_why": "A stunning, slow-paced journey through the rolling Nilgiri hills.", "best_time_to_visit": "10:00 AM"}
            },
            {
                "activity_name": "Doddabetta Peak Trek", "image_url": "https://images.unsplash.com/photo-1516690561799-2c7001ae37a2?w=800&q=80",
                "rating": 4.5, "category": "Nature • Viewpoint", "target_age_group": "Adults & Teens",
                "walking_effort": "High walk", "energy_level": "Active", "duration": "2 hrs", "best_time": "Early Morning",
                "tags": ["Trekking", "Panoramic Views"],
                "explainability": {"reason_why": "The highest peak in the Nilgiris offering breathtaking misty views.", "best_time_to_visit": "06:30 AM"}
            }
        ],
        "transportation": [
            {"mode": "Pre-booked Taxi", "duration": "Full Day", "cost_estimate": "₹2,500/day", "badges": ["Comfort", "Steep Roads"], "explainability": {"reason_why": "Best way to navigate the steep, winding roads safely.", "best_time_to_visit": None}},
            {"mode": "Auto Rickshaw", "duration": "Short Trips", "cost_estimate": "₹100-₹300", "badges": ["Local", "Budget"], "explainability": {"reason_why": "Good for quick trips around the main town area.", "best_time_to_visit": None}}
        ]
    }
