import React, { useState, useEffect, useContext } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { ThemeContext } from './_app';
import { generatePlan } from '../lib/api';
import { motion, AnimatePresence } from 'framer-motion';

const loadingSteps = [
  "Initializing TripMind Agents...",
  "Analyzing your travel preferences...",
  "Searching best destinations...",
  "Checking weather forecasts...",
  "Curating hotels and restaurants...",
  "Drafting optimal itinerary...",
  "Finalizing your premium trip..."
];

export default function PlanTrip() {
  const router = useRouter();
  const { isDark, toggleTheme } = useContext(ThemeContext);
  
  const [formData, setFormData] = useState({
    destination: '', 
    startDate: '', 
    endDate: '',
    kids: 0, 
    adults: 2, 
    seniors: 0,
    budget: '', 
    travelMode: 'Moderate', 
    food: 'Both', 
    style: 'Relaxed',
    interests: ['Nature', 'Food'] as string[]
  });
  
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [loadingStep, setLoadingStep] = useState(0);

  // Autocomplete state
  const [showDropdown, setShowDropdown] = useState(false);
  const popularCities = [
    "Goa, India",
    "Ooty, India",
    "Manali, India",
    "Bengaluru, India",
    "Jaipur, India",
    "Kochi, India",
    "Mumbai, India",
    "Delhi, India"
  ];

  const filteredCities = popularCities.filter(city => 
    city.toLowerCase().includes(formData.destination.toLowerCase())
  );

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (loading) {
      interval = setInterval(() => {
        setLoadingStep((prev) => Math.min(prev + 1, loadingSteps.length - 1));
      }, 4000);
    } else {
      setLoadingStep(0);
    }
    return () => clearInterval(interval);
  }, [loading]);

  const handleCounter = (field: 'kids' | 'adults' | 'seniors', operation: 'add' | 'sub') => {
    setFormData(prev => ({ ...prev, [field]: operation === 'add' ? prev[field] + 1 : Math.max(0, prev[field] - 1) }));
  };

  const toggleInterest = (interest: string) => {
    setFormData(prev => ({
      ...prev,
      interests: prev.interests.includes(interest) 
        ? prev.interests.filter(i => i !== interest)
        : [...prev.interests, interest]
    }));
  };

  const parseDateStr = (dateStr: string) => {
    if (/^\d{2}\/\d{2}\/\d{4}$/.test(dateStr)) {
      const parts = dateStr.split('/');
      return `${parts[2]}-${parts[1]}-${parts[0]}`;
    }
    return dateStr;
  };

  const handleSubmit = async () => {
    if (!formData.destination || !formData.startDate || !formData.endDate) {
      const missing = [];
      if (!formData.destination) missing.push('Destination');
      if (!formData.startDate) missing.push('Start Date');
      if (!formData.endDate) missing.push('End Date');
      setErrorMsg(`Please fill out: ${missing.join(', ')}`);
      return;
    }
    
    const parsedStart = parseDateStr(formData.startDate);
    const parsedEnd = parseDateStr(formData.endDate);

    const start = new Date(parsedStart);
    const end = new Date(parsedEnd);
    if (end < start) {
      setErrorMsg("End date cannot be before start date.");
      return;
    }
    setErrorMsg('');
    setLoading(true);
    setLoadingStep(0);
    try {
      const result = await generatePlan({
        destination: formData.destination,
        startDate: parsedStart,
        endDate: parsedEnd,
        kids: formData.kids,
        adults: formData.adults,
        seniors: formData.seniors,
        budgetMode: formData.travelMode,
        budget: formData.budget,
        foodPref: formData.food,
        travelStyle: formData.style,
        interests: formData.interests
      });
      if (result && result.trip_id) {
        router.push(`/dashboard/${result.trip_id}`);
      } else {
        throw new Error("Failed to extract trip ID from response.");
      }
    } catch (err: any) {
      setErrorMsg(err.message || 'An error occurred during generation.');
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-[#0B0F17] text-gray-900 dark:text-gray-100 flex flex-col items-center justify-center p-6 relative overflow-hidden transition-colors duration-300">
        <Head><title>Orchestrating Trip | TripMind AI</title></Head>
        
        {/* Decorative background glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-[#8B9CFF]/10 blur-[100px] rounded-full pointer-events-none"></div>

        <motion.div 
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="relative z-10 flex flex-col items-center max-w-md w-full"
        >
          {/* Animated Mascot / Spinner */}
          <div className="relative w-24 h-24 mb-10">
            <motion.div 
              animate={{ rotate: 360 }}
              transition={{ repeat: Infinity, duration: 8, ease: "linear" }}
              className="absolute inset-0 border-2 border-dashed border-[#8B9CFF]/40 rounded-full"
            />
            <motion.div 
              animate={{ rotate: -360 }}
              transition={{ repeat: Infinity, duration: 12, ease: "linear" }}
              className="absolute inset-2 border-2 border-dashed border-indigo-400/30 rounded-full"
            />
            <div className="absolute inset-0 flex items-center justify-center text-4xl">
              🧠
            </div>
          </div>
          
          <h2 className="text-3xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-500 dark:from-white dark:to-gray-400">
            TripMind is thinking
          </h2>

          <div className="w-full h-1.5 bg-gray-200 dark:bg-gray-800 rounded-full overflow-hidden mb-6">
            <motion.div 
              className="h-full bg-gradient-to-r from-indigo-500 to-[#8B9CFF]"
              initial={{ width: "0%" }}
              animate={{ width: `${((loadingStep + 1) / loadingSteps.length) * 100}%` }}
              transition={{ duration: 0.8, ease: "easeOut" }}
            />
          </div>

          <div className="h-8 relative w-full flex justify-center">
            <AnimatePresence mode="wait">
              <motion.p
                key={loadingStep}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.3 }}
                className="text-gray-500 dark:text-gray-400 text-center font-medium absolute"
              >
                {loadingSteps[loadingStep]}
              </motion.p>
            </AnimatePresence>
          </div>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white dark:bg-[#0B0F17] text-gray-900 dark:text-gray-100 pb-20 font-sans transition-colors duration-300">
      <Head>
        <title>New Trip | TripMind AI</title>
      </Head>

      {/* Top Navigation */}
      <nav className="border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-[#0B0F17]/80 backdrop-blur-md sticky top-0 z-50 px-6 py-4 flex justify-between items-center transition-colors duration-300">
        <a href="/" className="flex items-center gap-2 font-display font-bold text-xl hover:opacity-80 transition-opacity">
          <span className="text-[#8B9CFF]">TripMind</span> <span className="text-gray-900 dark:text-white">AI</span>
        </a>
        <div className="flex items-center gap-4 text-sm">
          <span className="hidden sm:flex items-center gap-2 text-gray-500 dark:text-gray-400">
            <span className="w-2 h-2 rounded-full bg-green-500"></span> Agentic AI • online
          </span>
          <button onClick={toggleTheme} className="w-8 h-8 flex items-center justify-center rounded-lg border border-gray-300 dark:border-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-[#1A1F2E] transition-colors">
            {isDark ? '☼' : '☾'}
          </button>
        </div>
      </nav>

      <main className="max-w-2xl mx-auto pt-12 px-6">
        <div className="mb-12">
          <p className="text-[#8B9CFF] text-xs font-bold tracking-widest uppercase mb-2">New Trip</p>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-3 transition-colors duration-300">Where are you headed?</h1>
          <p className="text-gray-500 dark:text-gray-400 text-base transition-colors duration-300">Tell us a bit about your group. TripMind will compose the rest.</p>
        </div>

        {errorMsg && (
          <div className="mb-6 p-4 bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400 rounded-xl">
            {errorMsg}
          </div>
        )}

        <div className="space-y-10">
          
          {/* Destination */}
          <section className="relative z-20">
            <label className="text-xs font-semibold text-gray-500 dark:text-gray-400 tracking-wider uppercase mb-3 block">Destination</label>
            <div className="relative">
              <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">📍</span>
              <input 
                type="text" placeholder="Search Indian cities..."
                className="w-full bg-white dark:bg-[#0B0F17] border border-gray-300 dark:border-gray-800 rounded-xl py-3.5 pl-10 pr-4 text-gray-900 dark:text-white focus:outline-none focus:border-[#8B9CFF] transition-colors"
                value={formData.destination} 
                onChange={(e) => {
                  setFormData({...formData, destination: e.target.value});
                  setShowDropdown(true);
                }}
                onFocus={() => setShowDropdown(true)}
                onBlur={() => setTimeout(() => setShowDropdown(false), 200)}
              />
              
              <AnimatePresence>
                {showDropdown && filteredCities.length > 0 && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="absolute top-full left-0 right-0 mt-2 bg-white dark:bg-[#151923] border border-gray-200 dark:border-gray-800 rounded-xl shadow-xl overflow-hidden z-50"
                  >
                    {filteredCities.map((city) => (
                      <div
                        key={city}
                        onClick={() => {
                          setFormData({...formData, destination: city});
                          setShowDropdown(false);
                        }}
                        className="px-4 py-3 hover:bg-gray-50 dark:hover:bg-[#1A1F2E] cursor-pointer flex items-center gap-3 transition-colors text-gray-900 dark:text-gray-200"
                      >
                        <span className="text-[#8B9CFF]">📍</span> {city}
                      </div>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </section>

          {/* Travel Dates */}
          <section>
            <label className="text-xs font-semibold text-gray-500 dark:text-gray-400 tracking-wider uppercase mb-3 block">Travel Dates</label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <span className="block text-xs text-gray-500 dark:text-gray-400 mb-1.5">Start date</span>
                <input 
                  type="text" 
                  placeholder="DD/MM/YYYY"
                  value={formData.startDate}
                  onChange={(e) => setFormData({...formData, startDate: e.target.value})}
                  className="w-full bg-transparent border border-gray-300 dark:border-gray-800 rounded-xl py-3.5 px-4 text-gray-900 dark:text-gray-300 focus:outline-none focus:border-[#8B9CFF]" 
                />
              </div>
              <div>
                <span className="block text-xs text-gray-500 dark:text-gray-400 mb-1.5">End date</span>
                <input 
                  type="text" 
                  placeholder="DD/MM/YYYY"
                  value={formData.endDate}
                  onChange={(e) => setFormData({...formData, endDate: e.target.value})}
                  className="w-full bg-transparent border border-gray-300 dark:border-gray-800 rounded-xl py-3.5 px-4 text-gray-900 dark:text-gray-300 focus:outline-none focus:border-[#8B9CFF]" 
                />
              </div>
            </div>
          </section>

          {/* Group Composition */}
          <section>
            <label className="text-xs font-semibold text-gray-500 dark:text-gray-400 tracking-wider uppercase mb-3 block">Group Composition</label>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {[
                { label: 'Kids', sub: '0-17', field: 'kids' },
                { label: 'Adults', sub: '18-49', field: 'adults' },
                { label: 'Seniors', sub: '50+', field: 'seniors' }
              ].map((group) => (
                <div key={group.label} className="bg-transparent border border-gray-300 dark:border-gray-800 rounded-xl p-4 flex flex-col items-center justify-center transition-colors duration-300">
                  <span className="font-semibold text-gray-900 dark:text-white text-sm">{group.label}</span>
                  <span className="text-xs text-gray-400 dark:text-gray-500 mb-4">{group.sub}</span>
                  <div className="flex items-center gap-4">
                    <button onClick={() => handleCounter(group.field as any, 'sub')} className="w-8 h-8 rounded-full bg-gray-100 dark:bg-[#151923] text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white flex items-center justify-center border border-gray-200 dark:border-gray-800 transition-colors">-</button>
                    <span className="text-lg font-bold w-4 text-center text-gray-900 dark:text-white">{formData[group.field as keyof typeof formData]}</span>
                    <button onClick={() => handleCounter(group.field as any, 'add')} className="w-8 h-8 rounded-full bg-gray-100 dark:bg-[#151923] text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white flex items-center justify-center border border-gray-200 dark:border-gray-800 transition-colors">+</button>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Total Budget */}
          <section>
            <label className="text-xs font-semibold text-gray-500 dark:text-gray-400 tracking-wider uppercase mb-3 block">Total Budget (Optional)</label>
            <div className="relative">
              <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">₹</span>
              <input 
                type="number" placeholder="e.g. 150000"
                className="w-full bg-transparent border border-gray-300 dark:border-gray-800 rounded-xl py-3.5 pl-8 pr-4 text-gray-900 dark:text-white focus:outline-none focus:border-[#8B9CFF] transition-colors"
                value={formData.budget} onChange={(e) => setFormData({...formData, budget: e.target.value})}
              />
            </div>
          </section>

          {/* Travel Mode (Cards) */}
          <section>
            <label className="text-xs font-semibold text-gray-500 dark:text-gray-400 tracking-wider uppercase mb-3 block">Travel Mode</label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {[
                { title: 'Budget', desc: 'Best value, simple stays' },
                { title: 'Moderate', desc: 'Comfortable mid-range' },
                { title: 'Premium', desc: '4-star resorts, fine dining' },
                { title: 'Luxury', desc: '5-star, private experiences' }
              ].map(mode => (
                <div 
                  key={mode.title} 
                  onClick={() => setFormData({...formData, travelMode: mode.title})}
                  className={`cursor-pointer rounded-xl p-4 border transition-all ${formData.travelMode === mode.title ? 'border-[#8B9CFF] bg-[#8B9CFF]/5 dark:bg-[#8B9CFF]/10' : 'border-gray-300 dark:border-gray-800 bg-transparent hover:border-gray-400 dark:hover:border-gray-700'}`}
                >
                  <h3 className={`font-semibold text-sm mb-1 ${formData.travelMode === mode.title ? 'text-[#8B9CFF]' : 'text-gray-900 dark:text-white'}`}>{mode.title}</h3>
                  <p className="text-[10px] text-gray-500 dark:text-gray-400 leading-tight">{mode.desc}</p>
                </div>
              ))}
            </div>
          </section>

          {/* Food Preference */}
          <section>
            <label className="text-xs font-semibold text-gray-500 dark:text-gray-400 tracking-wider uppercase mb-3 block">Food Preference</label>
            <div className="flex flex-wrap gap-3">
              {['Veg', 'Non-Veg', 'Both', 'Vegan'].map(opt => (
                <button 
                  key={opt} onClick={() => setFormData({...formData, food: opt})}
                  className={`px-5 py-2 rounded-full border text-sm transition-colors ${formData.food === opt ? 'border-[#8B9CFF] text-[#8B9CFF] bg-[#8B9CFF]/5 dark:bg-[#8B9CFF]/10' : 'bg-transparent border-gray-300 dark:border-gray-800 text-gray-600 dark:text-gray-300 hover:border-gray-400 dark:hover:border-gray-700'}`}
                >
                  {opt}
                </button>
              ))}
            </div>
          </section>

          {/* Travel Style */}
          <section>
            <label className="text-xs font-semibold text-gray-500 dark:text-gray-400 tracking-wider uppercase mb-3 block">Travel Style</label>
            <div className="flex flex-wrap gap-3">
              {['Relaxed', 'Adventure', 'Family', 'Luxury', 'Budget', 'Balanced'].map(opt => (
                <button 
                  key={opt} onClick={() => setFormData({...formData, style: opt})}
                  className={`px-5 py-2 rounded-full border text-sm transition-colors ${formData.style === opt ? 'border-[#8B9CFF] text-[#8B9CFF] bg-[#8B9CFF]/5 dark:bg-[#8B9CFF]/10' : 'bg-transparent border-gray-300 dark:border-gray-800 text-gray-600 dark:text-gray-300 hover:border-gray-400 dark:hover:border-gray-700'}`}
                >
                  {opt}
                </button>
              ))}
            </div>
          </section>

          {/* Interests */}
          <section>
            <label className="text-xs font-semibold text-gray-500 dark:text-gray-400 tracking-wider uppercase mb-3 block">Interests</label>
            <div className="flex flex-wrap gap-3">
              {[
                { label: 'Nature', icon: '🌲' }, { label: 'Food', icon: '☕' }, 
                { label: 'Shopping', icon: '🛍️' }, { label: 'History', icon: '🏛️' }, 
                { label: 'Photography', icon: '📷' }, { label: 'Nightlife', icon: '🌙' },
                { label: 'Beaches', icon: '🏖️' }
              ].map(opt => {
                const isActive = formData.interests.includes(opt.label);
                return (
                  <button 
                    key={opt.label} onClick={() => toggleInterest(opt.label)}
                    className={`px-4 py-2 rounded-full border text-sm flex items-center gap-2 transition-colors ${isActive ? 'border-[#8B9CFF] text-[#8B9CFF] bg-[#8B9CFF]/5 dark:bg-[#8B9CFF]/10' : 'bg-transparent border-gray-300 dark:border-gray-800 text-gray-600 dark:text-gray-300 hover:border-gray-400 dark:hover:border-gray-700'}`}
                  >
                    <span>{opt.icon}</span> {opt.label}
                  </button>
                );
              })}
            </div>
          </section>

          {/* Action Button */}
          <div className="pt-8 border-t border-gray-200 dark:border-gray-800">
            <button 
              onClick={handleSubmit}
              className="block w-full bg-[#8B9CFF] hover:bg-[#7A8CE6] text-black text-center font-semibold text-lg py-4 px-6 rounded-xl transition-colors shadow-[0_0_20px_rgba(139,156,255,0.2)]"
            >
              ✨ Generate my trip →
            </button>
          </div>

        </div>
      </main>
    </div>
  );
}