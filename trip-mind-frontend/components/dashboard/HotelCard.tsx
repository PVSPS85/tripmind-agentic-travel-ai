import { motion } from 'framer-motion';

interface HotelProps {
  hotel: {
    name: string;
    rating: string;
    location: string;
    price: string;
    tags: string[];
    aiReason: string;
    imageUrl: string;
  }
}

export default function HotelCard({ hotel }: HotelProps) {
  return (
    <motion.div 
      whileHover={{ y: -2 }}
      className="flex flex-col sm:flex-row bg-surface border border-border rounded-card overflow-hidden shadow-soft group"
    >
      <div className="w-full sm:w-48 h-48 sm:h-auto bg-surface2">
        <img src={hotel.imageUrl} alt={hotel.name} className="w-full h-full object-cover" />
      </div>
      <div className="p-5 flex flex-col justify-between flex-grow">
        <div>
          <div className="flex justify-between items-start mb-2">
            <h4 className="font-display font-bold text-lg">{hotel.name}</h4>
            <span className="font-mono text-sm bg-primary-soft text-primary px-2 py-1 rounded-tag">
              ⭐ {hotel.rating}
            </span>
          </div>
          <p className="text-subtle text-sm mb-3">{hotel.location}</p>
          
          <div className="flex flex-wrap gap-2 mb-4">
            {hotel.tags.map((tag, i) => (
              <span key={i} className="text-xs bg-surface2 text-muted px-2 py-1 rounded-tag border border-border">
                {tag}
              </span>
            ))}
          </div>
        </div>
        
        <div className="flex items-end justify-between mt-4 border-t border-border pt-4">
          <div>
            <p className="text-xs font-medium text-accent mb-1 flex items-center">
              <span className="mr-1">✨</span> Why this place:
            </p>
            <p className="text-sm text-muted line-clamp-2">{hotel.aiReason}</p>
          </div>
          <div className="text-right ml-4 shrink-0">
            <p className="font-mono font-bold text-foreground">{hotel.price}</p>
            <p className="text-xs text-subtle">per night</p>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
