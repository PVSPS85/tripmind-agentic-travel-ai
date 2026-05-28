from typing import Dict

class BudgetLogic:
    """Financial guardrails for INR-based travel planning."""

    @staticmethod
    def get_allocation_targets(total_budget: float) -> Dict[str, float]:
        """Defines the safe spending brackets for the Agent to follow."""
        return {
            "stay": total_budget * 0.45,       # 45% for Hotels
            "food": total_budget * 0.20,       # 20% for Dining
            "transit": total_budget * 0.15,    # 15% for Local Cabs/Auto
            "activities": total_budget * 0.10, # 10% for Tickets/Entry
            "buffer": total_budget * 0.10      # 10% Emergency Cash
        }

    @staticmethod
    def verify_safety_limit(current_total: float, max_limit: float) -> bool:
        """Final check to ensure the generated plan is within budget."""
        return current_total <= max_limit
