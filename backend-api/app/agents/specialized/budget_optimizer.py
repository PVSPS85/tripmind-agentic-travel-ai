from typing import Dict

class BudgetLogic:
    """Financial guardrails for INR-based travel planning."""

    @staticmethod
    def get_allocation_targets(total_budget: float) -> Dict[str, float]:
        """Defines the safe spending brackets for the Agent to follow."""
        return {
            # Keys expected by crew.py
            "accommodation_target": total_budget * 0.45,
            "food_target": total_budget * 0.20,
            "activity_target": total_budget * 0.10,
            "transport_target": total_budget * 0.15,
            "contingency_buffer": total_budget * 0.10,
            # Original keys (kept for backward compatibility)
            "stay": total_budget * 0.45,
            "food": total_budget * 0.20,
            "transit": total_budget * 0.15,
            "activities": total_budget * 0.10,
            "buffer": total_budget * 0.10
        }

    # Alias so both names work
    calculate_target_allocations = get_allocation_targets

    @staticmethod
    def verify_safety_limit(current_total: float, max_limit: float) -> bool:
        """Final check to ensure the generated plan is within budget."""
        return current_total <= max_limit
