from typing import Dict, Any

class ProfileLogic:
    """Hard-coded constraints for demographic safety and pacing."""
    
    @staticmethod
    def calculate_pacing_constraints(travelers: Dict[str, int]) -> Dict[str, Any]:
        kids = travelers.get("kids", 0)
        seniors = travelers.get("seniors", 0)
        adults = travelers.get("adults", 1)
        
        # Determine the 'Brake Factor' — higher means more rest stops required
        brake_factor = (kids * 1.5) + (seniors * 2.0)
        
        # Determine pace label
        if brake_factor >= 4.0:
            pace_label = "Slow & Gentle"
            max_active_hours = 4
        elif brake_factor >= 2.0:
            pace_label = "Moderate"
            max_active_hours = 6
        else:
            pace_label = "Active"
            max_active_hours = 8
        
        constraints = {
            # Keys expected by crew.py
            "pace_label": pace_label,
            "max_active_hours": max_active_hours,
            "requires_accessibility": seniors > 0,
            "is_child_friendly": kids > 0,
            # Original detailed keys
            "max_walking_km_per_day": 5.0 if seniors > 0 else 10.0,
            "required_rest_stops": "Frequent" if (kids > 0 or seniors > 0) else "Minimal",
            "nap_window_required": True if kids > 0 and kids < 5 else False,
            "senior_mobility_access": True if seniors > 0 else False
        }
        
        return constraints

    # Alias so both names work
    determine_pacing_constraints = calculate_pacing_constraints
