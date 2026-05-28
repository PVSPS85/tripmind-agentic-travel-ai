import React from 'react';

interface CounterInputProps {
  label: string;
  subtitle?: string;
  value: number;
  onChange: (val: number) => void;
  min?: number;
  max?: number;
}

export default function CounterInput({
  label,
  subtitle,
  value,
  onChange,
  min = 0,
  max = 20
}: CounterInputProps) {
  return (
    <div className="bg-surface border border-border p-4 rounded-card shadow-sm flex flex-col justify-between h-full">
      <div className="mb-3">
        <label className="block text-sm font-medium text-foreground capitalize">
          {label}
        </label>
        {subtitle && (
          <span className="block text-xs text-subtle mt-0.5">
            {subtitle}
          </span>
        )}
      </div>
      
      <div className="flex items-center justify-between mt-auto bg-surface2 rounded-btn border border-border overflow-hidden">
        <button 
          type="button" 
          onClick={() => onChange(Math.max(min, value - 1))}
          disabled={value <= min}
          className="px-4 py-2 hover:bg-border transition-colors text-muted hover:text-foreground disabled:opacity-40 disabled:cursor-not-allowed"
          aria-label={`Decrease ${label}`}
        >
          -
        </button>
        
        <span className="font-mono text-sm font-medium w-8 text-center text-foreground">
          {value}
        </span>
        
        <button 
          type="button" 
          onClick={() => onChange(Math.min(max, value + 1))}
          disabled={value >= max}
          className="px-4 py-2 hover:bg-border transition-colors text-muted hover:text-foreground disabled:opacity-40 disabled:cursor-not-allowed"
          aria-label={`Increase ${label}`}
        >
          +
        </button>
      </div>
    </div>
  );
}
