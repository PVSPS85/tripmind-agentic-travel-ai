import { useState, useRef, useEffect } from 'react';

interface SearchBarProps {
  value: string;
  onChange: (val: string) => void;
}

export default function SearchBar({ value, onChange }: SearchBarProps) {
  const [isOpen, setIsOpen] = useState(false);
  const wrapperRef = useRef<HTMLDivElement>(null);
  
  // Test locations specified in the Figma prompt
  const suggestions = ["Goa, India", "Manali, India", "Jaipur, India", "Ooty, India", "Bengaluru, India", "Kochi, India"];

  // Close dropdown if user clicks outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div ref={wrapperRef} className="relative w-full">
      <label className="block text-sm font-medium text-muted mb-2">Destination</label>
      <input
        type="text"
        value={value}
        onChange={(e) => {
          onChange(e.target.value);
          setIsOpen(true);
        }}
        onFocus={() => setIsOpen(true)}
        placeholder="e.g., Goa, Manali, Jaipur..."
        className="w-full p-3 rounded-btn border border-border bg-surface focus:outline-none focus:border-primary transition-colors text-foreground shadow-sm"
      />
      
      {/* Autocomplete Dropdown */}
      {isOpen && value.length > 0 && (
        <ul className="absolute z-10 w-full mt-2 bg-surface border border-border rounded-btn shadow-soft max-h-48 overflow-auto">
          {suggestions
            .filter(s => s.toLowerCase().includes(value.toLowerCase()))
            .map((place, i) => (
              <li 
                key={i} 
                onClick={() => {
                  onChange(place);
                  setIsOpen(false);
                }}
                className="p-3 hover:bg-surface2 cursor-pointer text-sm text-foreground transition-colors flex items-center gap-2"
              >
                <span className="text-muted">📍</span> {place}
              </li>
          ))}
        </ul>
      )}
    </div>
  );
}
