const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api/v1';

export interface TripRequest {
  destination: string;
  startDate: string;
  endDate: string;
  kids: number;
  adults: number;
  seniors: number;
  budget?: string;
  budgetMode: string;
  foodPref: string;
  travelStyle: string;
  interests: string[];
}

function computeBudgetINR(data: TripRequest): number {
  // If user typed a specific budget, use it
  if (data.budget && parseInt(data.budget) > 0) {
    return parseInt(data.budget);
  }
  // Otherwise, derive from budgetMode
  switch (data.budgetMode) {
    case 'Luxury': return 200000;
    case 'Premium': return 120000;
    case 'Moderate': return 75000;
    case 'Budget': return 30000;
    default: return 75000;
  }
}

export async function generatePlan(data: TripRequest) {
  const backendPayload = {
    destination: data.destination,
    start_date: data.startDate,
    end_date: data.endDate,
    travelers: {
      kids: data.kids,
      adults: data.adults,
      seniors: data.seniors
    },
    budget_inr: computeBudgetINR(data),
    food_preference: data.foodPref,
    travel_style: data.travelStyle,
    interests: data.interests
  };

  try {
    const response = await fetch(`${API_URL}/plan`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(backendPayload),
    });
    
    if (!response.ok) {
      let errorMsg = 'Failed to generate trip';
      try {
        const errorData = await response.json();
        errorMsg = errorData.error || errorMsg;
      } catch (e) {
        errorMsg = `Server error (${response.status}). The AI orchestration may have timed out or failed.`;
      }
      throw new Error(errorMsg);
    }
    return await response.json();
  } catch (err: any) {
    if (err.message === 'Failed to fetch') {
      throw new Error("Unable to connect to the backend server. Please ensure the API is running on port 8000.");
    }
    throw err;
  }
}

export async function fetchDashboard(tripId: string) {
  try {
    const response = await fetch(`${API_URL}/trips/${tripId}`);
    if (!response.ok) {
      if (response.status === 404) throw new Error("This trip doesn't exist or hasn't finished generating.");
      throw new Error("Failed to load dashboard data from the server.");
    }
    return await response.json();
  } catch (err: any) {
    if (err.message === 'Failed to fetch') {
      throw new Error("Unable to connect to the backend server. Please ensure the API is running on port 8000.");
    }
    throw err;
  }
}
