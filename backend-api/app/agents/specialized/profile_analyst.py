from typing import Dict, Any

class ProfileLogic:
    """Hard-coded constraints for demographic safety and pacing."""
    
    @staticmethod
    def calculate_pacing_constraints(travelers: Dict[str, int]) -> Dict[str, Any]:
        kids = travelers.get("kids", 0)
        seniors = travelers.get("seniors", 0)
        
        # Determine the 'Brake Factor' — higher means more rest stops required
        brake_factor = (kids * 1.5) + (seniors * 2.0)
        
        constraints = {
            "max_walking_km_per_day": 5.0 if seniors > 0 else 10.0,
            "required_rest_stops": "Frequent" if (kids > 0 or seniors > 0) else "Minimal",
            "nap_window_required": True if kids > 0 and kids < 5 else False,
            "senior_mobility_access": True if seniors > 0 else False
        }
        
        return constraints
