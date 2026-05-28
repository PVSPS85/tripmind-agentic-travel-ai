import pytest
from app.agents.specialized.budget_optimizer import BudgetOptimizerLogic

def test_budget_percentage_allocation_calculations() -> None:
    """
    Verifies that baseline Indian hospitality economic multipliers parse absolute 
    INR figures accurately across granular service brackets.
    """
    test_budget_inr = 200000.0  # ₹2,00,000 INR Allocation
    calculated_targets = BudgetOptimizerLogic.calculate_target_allocations(test_budget_inr)
    
    # Assert exact proportional distributions (40% Hotels, 25% Dining, 20% Attractions, 10% Transport, 5% Cache Buffer)
    assert calculated_targets["accommodation_target"] == 80000.0
    assert calculated_targets["food_target"] == 50000.0
    assert calculated_targets["activity_target"] == 40000.0
    assert calculated_targets["transport_target"] == 20000.0
    assert calculated_targets["contingency_buffer"] == 10000.0

def test_budget_compliance_boundary_checks() -> None:
    """
    Validates boundary criteria mapping logic ensuring financial ceilings reject budget overruns.
    """
    is_under_budget = BudgetOptimizerLogic.validate_budget_compliance(allocated=145000.0, limit=150000.0)
    assert is_under_budget is True
    
    is_over_budget = BudgetOptimizerLogic.validate_budget_compliance(allocated=162000.0, limit=150000.0)
    assert is_over_budget is False
