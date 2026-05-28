import React, { useState, useContext } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { ThemeContext } from './_app';

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

        <div className="space-y-10">
          
          {/* Destination */}
          <section>
            <label className="text-xs font-semibold text-gray-500 dark:text-gray-400 tracking-wider uppercase mb-3 block">Destination</label>
            <div className="relative">
              <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">📍</span>
              <input 
                type="text" placeholder="Search Indian cities..."
                className="w-full bg-transparent border border-gray-300 dark:border-gray-800 rounded-xl py-3.5 pl-10 pr-4 text-gray-900 dark:text-white focus:outline-none focus:border-[#8B9CFF] transition-colors"
                value={formData.destination} onChange={(e) => setFormData({...formData, destination: e.target.value})}
              />
            </div>
          </section>

          {/* Travel Dates */}
          <section>
            <label className="text-xs font-semibold text-gray-500 dark:text-gray-400 tracking-wider uppercase mb-3 block">Travel Dates</label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <span className="block text-xs text-gray-500 dark:text-gray-400 mb-1.5">Start date</span>
                <input type="date" className="w-full bg-transparent border border-gray-300 dark:border-gray-800 rounded-xl py-3.5 px-4 text-gray-900 dark:text-gray-300 focus:outline-none focus:border-[#8B9CFF]" />
              </div>
              <div>
                <span className="block text-xs text-gray-500 dark:text-gray-400 mb-1.5">End date</span>
                <input type="date" className="w-full bg-transparent border border-gray-300 dark:border-gray-800 rounded-xl py-3.5 px-4 text-gray-900 dark:text-gray-300 focus:outline-none focus:border-[#8B9CFF]" />
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
            <label className="text-xs font-semibold text-gray-500 dark:text-gray-400 tracking-wider uppercase mb-3 block">Total Budget</label>
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
              {['Veg', 'Non-Veg', 'Both'].map(opt => (
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
              {['Relaxed', 'Adventure', 'Family', 'Luxury', 'Budget'].map(opt => (
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
                { label: 'Photography', icon: '📷' }, { label: 'Nightlife', icon: '🌙' }
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
            <a 
              href="/dashboard/123"
              className="block w-full bg-[#8B9CFF] hover:bg-[#7A8CE6] text-black text-center font-semibold text-lg py-4 px-6 rounded-xl transition-colors shadow-[0_0_20px_rgba(139,156,255,0.2)]"
            >
              ✨ Generate my trip →
            </a>
          </div>

        </div>
      </main>
    </div>
  );
}