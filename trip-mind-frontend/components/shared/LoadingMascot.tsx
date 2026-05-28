import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';

const steps = [
  "Analyzing travelers",
  "Checking weather",
  "Searching hotels",
  "Searching food",
  "Building itinerary",
  "Optimizing budget",
  "Planning transport",
  "Finalizing trip plan"
];

export default function LoadingMascot() {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep((prev) => (prev < steps.length - 1 ? prev + 1 : prev));
    }, 1200); // Progresses through steps automatically for the demo
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center relative overflow-hidden dark">
      {/* Background Glow */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_#1E1B4B_0%,_#0D0F14_70%)] -z-10" />

      {/* Animated Mascot / AI Indicator */}
      <motion.div 
        animate={{ y: [0, -10, 0] }}
        transition={{ repeat: Infinity, duration: 2, ease: "easeInOut" }}
        className="w-24 h-24 mb-12 rounded-full bg-indigo-500/20 flex items-center justify-center border border-indigo-500/30 shadow-[0_0_40px_rgba(79,70,229,0.3)]"
      >
        <span className="text-4xl">🐰</span> {/* Tasteful placeholder mascot */}
      </motion.div>

      {/* Progress Steps */}
      <div className="w-full max-w-md space-y-4">
        {steps.map((step, index) => {
          const isActive = index === currentStep;
          const isPast = index < currentStep;
          
          return (
            <motion.div 
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: isPast || isActive ? 1 : 0.3, x: 0 }}
              className={`flex items-center space-x-3 ${isActive ? 'text-teal-400' : 'text-gray-400'}`}
            >
              <div className={`w-5 h-5 rounded-full flex items-center justify-center text-xs
                ${isPast ? 'bg-teal-500 text-white' : isActive ? 'bg-teal-500/20 border border-teal-500' : 'bg-gray-800'}`}
              >
                {isPast ? '✓' : ''}
              </div>
              <span className={`font-medium ${isActive ? 'text-white' : ''}`}>{step}</span>
            </motion.div>
          );
        })}
      </div>
      
      {/* Progress Bar */}
      <div className="w-full max-w-md mt-8 h-1 bg-gray-800 rounded-full overflow-hidden">
        <motion.div 
          className="h-full bg-indigo-500"
          initial={{ width: '0%' }}
          animate={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
          transition={{ ease: "easeInOut" }}
        />
      </div>
    </div>
  );
}
