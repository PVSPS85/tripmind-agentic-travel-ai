export interface TripRequest {
  destination: string;
  kids: number;
  adults: number;
  seniors: number;
  budgetMode: string;
  foodPref: string;
  travelStyle: string;
}

export async function generatePlan(data: TripRequest) {
  const response = await fetch('/api/plan', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  
  if (!response.ok) throw new Error('Failed to generate trip');
  return response.json();
}

export async function fetchDashboard(tripId: string) {
  const response = await fetch(`/api/plan?tripId=${tripId}`);
  if (!response.ok) throw new Error('Trip not found');
  return response.json();
}
