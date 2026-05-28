from typing import List, Dict

class ItineraryLogic:
    """Utility to ensure chronological and geographic sanity."""

    @staticmethod
    def validate_time_slots(activities: List[Dict]) -> bool:
        """Ensures Morning -> Afternoon -> Evening flow without overlaps."""
        slots = [a.get("time_slot").lower() for a in activities]
        order = {"morning": 1, "afternoon": 2, "evening": 3}
        
        # Check if the generated slots are in strictly ascending order
        current_rank = 0
        for slot in slots:
            rank = order.get(slot, 0)
            if rank <= current_rank:
                return False
            current_rank = rank
        return True
