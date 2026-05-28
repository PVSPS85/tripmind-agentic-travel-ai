export default function ItineraryDayCard({ day }: { day: any }) {
  return (
    <div className="bg-surface border border-border rounded-card p-5 shadow-sm">
      <div className="flex justify-between items-center border-b border-border pb-3 mb-4">
        <div>
          <span className="text-xs font-bold text-primary uppercase tracking-wider">Day {day.day}</span>
          <h3 className="font-display text-lg font-bold">{day.title}</h3>
        </div>
        <div className="flex items-center space-x-2 bg-surface2 px-3 py-1.5 rounded-tag">
          <span>🌧️</span>
          <span className="text-sm font-mono">{day.weather}</span>
        </div>
      </div>

      <div className="space-y-4">
        {/* Placeholder for Morning / Afternoon / Evening events */}
        <div className="relative pl-6 border-l-2 border-border">
          <div className="absolute w-3 h-3 bg-accent rounded-full -left-[7px] top-1"></div>
          <h4 className="font-medium text-sm">Morning: Basilica of Bom Jesus</h4>
          <p className="text-xs text-muted mt-1">Indoor activity: Best to visit before the crowds. No stairs, highly accessible.</p>
        </div>
        
        {/* Transport Chip */}
        <div className="pl-6 py-1">
          <span className="inline-flex items-center text-xs bg-surface2 border border-border px-2 py-1 rounded-tag text-muted">
            🚕 15 min cab ride (est. ₹300)
          </span>
        </div>

        <div className="relative pl-6 border-l-2 border-border">
          <div className="absolute w-3 h-3 bg-primary rounded-full -left-[7px] top-1"></div>
          <h4 className="font-medium text-sm">Afternoon: Authentic Goan Lunch</h4>
          <p className="text-xs text-accent mt-1">✨ AI Note: Swapped outdoor beach to indoor dining due to expected 2PM rain.</p>
        </div>
      </div>
    </div>
  );
}
