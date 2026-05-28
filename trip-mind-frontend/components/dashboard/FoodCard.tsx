import { motion } from 'framer-motion';

interface FoodProps {
  food: {
    name: string;
    cuisine: string;
    dietary: 'Veg' | 'Non-Veg' | 'Both';
    rating: string;
    distance: string;
    aiReason: string;
    imageUrl: string;
  }
}

export default function FoodCard({ food }: FoodProps) {
  // Map dietary preference to the specific color tokens required
  const badgeStyle = 
    food.dietary === 'Veg' ? 'text-success bg-success/10 border-success/20' : 
    food.dietary === 'Non-Veg' ? 'text-destructive bg-destructive/10 border-destructive/20' : 
    'text-accent bg-accent/10 border-accent/20';

  return (
    <motion.div 
      whileHover={{ y: -2 }}
      className="flex flex-col sm:flex-row bg-surface border border-border rounded-card overflow-hidden shadow-soft group"
    >
      <div className="w-full sm:w-40 h-40 sm:h-auto bg-surface2 shrink-0">
        <img src={food.imageUrl} alt={food.name} className="w-full h-full object-cover" />
      </div>
      
      <div className="p-4 flex flex-col justify-between flex-grow">
        <div>
          <div className="flex justify-between items-start mb-1">
            <h4 className="font-display font-bold text-lg">{food.name}</h4>
            <button className="text-subtle hover:text-accent transition-colors" aria-label="Save this restaurant">
              {/* Bookmark Icon */}
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
              </svg>
            </button>
          </div>
          
          <div className="flex items-center gap-3 mb-3">
            <span className="font-mono text-xs bg-surface2 text-muted px-2 py-1 rounded-tag border border-border">
              ⭐ {food.rating}
            </span>
            <span className="text-sm text-subtle">{food.cuisine}</span>
            <span className="text-muted text-xs">•</span>
            <span className={`text-xs px-2 py-0.5 rounded-tag border ${badgeStyle}`}>
              {food.dietary}
            </span>
          </div>
        </div>
        
        {/* Explainable AI Block */}
        <div className="mt-2 bg-primary-soft/40 rounded-btn p-3 border border-primary/10">
          <p className="text-xs font-medium text-primary mb-1 flex items-center">
            <span className="mr-1">🤖</span> AI Reason
          </p>
          <p className="text-sm text-muted line-clamp-2">{food.aiReason}</p>
        </div>
      </div>
    </motion.div>
  );
}
