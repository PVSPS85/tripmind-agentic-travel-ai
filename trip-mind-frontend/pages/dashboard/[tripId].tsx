import React, { useState, useEffect, useContext } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { ThemeContext } from '../_app';
import { fetchDashboard } from '../../lib/api';
import { motion } from 'framer-motion';

export default function Dashboard() {
  const router = useRouter();
  const { tripId } = router.query;
  const { isDark, toggleTheme } = useContext(ThemeContext);
  
  const [tripData, setTripData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [openSections, setOpenSections] = useState<{[key: string]: boolean}>({
    hotels: true,
    food: true,
    transport: true,
    activities: true,
  });

  useEffect(() => {
    if (tripId) {
      setLoading(true);
      fetchDashboard(tripId as string)
        .then(data => {
          setTripData(data);
          setLoading(false);
        })
        .catch(err => {
          setError(err.message || 'Failed to load trip');
          setLoading(false);
        });
    }
  }, [tripId]);

  const handleExport = () => {
    window.print();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-[#0B0F17] flex items-center justify-center p-6 text-gray-900 dark:text-gray-100">
        <Head><title>Loading Dashboard | TripMind AI</title></Head>
        <div className="flex flex-col items-center">
          <div className="w-12 h-12 border-4 border-indigo-200 dark:border-[#8B9CFF]/30 border-t-indigo-600 dark:border-t-[#8B9CFF] rounded-full animate-spin mb-4"></div>
          <p className="text-gray-500 font-medium">Decrypting your optimized itinerary...</p>
        </div>
      </div>
    );
  }

  if (error || !tripData) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-[#0B0F17] flex items-center justify-center p-6 text-gray-900 dark:text-gray-100">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-2">Trip Not Found</h2>
          <p className="text-gray-500 mb-6">{error}</p>
          <a href="/plan" className="px-6 py-2 bg-indigo-600 dark:bg-[#8B9CFF] text-white dark:text-black font-semibold rounded-xl">Plan a new trip</a>
        </div>
      </div>
    );
  }

  const itineraryDays = Array.isArray(tripData.itinerary) ? tripData.itinerary : [];
  const hotels = Array.isArray(tripData.hotels) ? tripData.hotels : [];
  const foods = Array.isArray(tripData.food_and_dining) ? tripData.food_and_dining : [];
  const transports = Array.isArray(tripData.transportation) ? tripData.transportation : [];
  const extraActivities = Array.isArray(tripData.extra_activities) ? tripData.extra_activities : [];

  const bIntell = tripData.budget_intelligence || {};
  const totalAllocated = (bIntell.allocated_hotels_total_inr || 0) + (bIntell.allocated_food_total_inr || 0) + (bIntell.allocated_activities_total_inr || 0) + (bIntell.allocated_transport_total_inr || 0);
  const targetBudget = totalAllocated + (bIntell.remaining_buffer_inr || 0);

  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.15,
        delayChildren: 0.1,
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 30, scale: 0.98 },
    show: { 
      opacity: 1, 
      y: 0, 
      scale: 1,
      transition: { type: "spring", stiffness: 120, damping: 20 }
    }
  };

  const cardHoverVariants = {
    rest: { scale: 1 },
    hover: { 
      scale: 1.02,
      y: -4,
      boxShadow: "0px 10px 30px rgba(139, 156, 255, 0.15)",
      transition: { type: "spring", stiffness: 400, damping: 25 }
    }
  };

  return (
    <div className="min-h-screen bg-[#F8F9FA] dark:bg-[#0B0F17] text-gray-900 dark:text-gray-100 pb-20 font-sans transition-colors duration-300">
      <Head>
        <title>{tripData.destination} | TripMind AI</title>
      </Head>

      <nav className="border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-[#0B0F17] sticky top-0 z-50 px-6 py-4 flex justify-between items-center transition-colors duration-300 print:hidden">
        <a href="/" className="flex items-center gap-2 font-display font-bold text-xl hover:opacity-80 transition-opacity">
          <span className="text-indigo-600 dark:text-[#8B9CFF]">TripMind</span> <span className="text-gray-900 dark:text-white">AI</span>
        </a>
        <div className="flex items-center gap-4 text-sm font-medium">
          <span className="hidden sm:flex items-center gap-2 text-gray-600 dark:text-gray-400">
            <span className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]"></span> Agentic AI • online
          </span>
          <button onClick={toggleTheme} className="w-8 h-8 flex items-center justify-center rounded-lg border border-gray-200 dark:border-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-[#1A1F2E] transition-colors">
            {isDark ? '☼' : '☾'}
          </button>
        </div>
      </nav>

      <motion.main variants={containerVariants} initial="hidden" animate="show" className="max-w-[1200px] mx-auto px-4 sm:px-6 pt-10 pb-16 space-y-8">
        
        {/* HEADER BENTO */}
        <motion.div variants={itemVariants} className="flex flex-col md:flex-row justify-between items-start md:items-end gap-6 mb-4">
          <div>
            <p className="text-indigo-600 dark:text-[#8B9CFF] text-xs font-bold tracking-widest uppercase mb-2">YOUR TRIP PLAN</p>
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-2">{tripData.destination}</h1>
            <p className="text-gray-500 dark:text-gray-400 text-sm font-medium">
              {tripData.duration_days} days • {Math.max(1, tripData.duration_days - 1)} nights • {tripData.groupDynamics || 'Custom Group'}
            </p>
          </div>
          <div className="flex gap-3 w-full md:w-auto print:hidden">
            <button onClick={handleExport} className="px-5 py-2.5 rounded-xl border border-gray-200 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-[#151923] transition flex items-center justify-center gap-2 font-medium bg-white dark:bg-[#0B0F17] shadow-sm text-sm">
              ↓ Export
            </button>
            <a href="/plan" className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white transition flex items-center justify-center gap-2 font-semibold shadow-md text-sm">
              ✨ New trip
            </a>
          </div>
        </motion.div>

        {/* STATS BENTO ROW */}
        <motion.div variants={itemVariants} className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-white dark:bg-[#151923] p-5 rounded-2xl border border-gray-200 dark:border-gray-800 shadow-sm flex flex-col justify-center">
            <p className="text-xs text-gray-500 font-semibold uppercase tracking-wider mb-1 flex items-center gap-2">🗓 DATES</p>
            <p className="text-sm font-semibold text-gray-900 dark:text-white">Generated Plan</p>
          </div>
          <div className="bg-white dark:bg-[#151923] p-5 rounded-2xl border border-gray-200 dark:border-gray-800 shadow-sm flex flex-col justify-center">
            <p className="text-xs text-gray-500 font-semibold uppercase tracking-wider mb-1 flex items-center gap-2">👥 TRAVELERS</p>
            <p className="text-sm font-semibold text-gray-900 dark:text-white">Custom Profile</p>
          </div>
          <div className="bg-white dark:bg-[#151923] p-5 rounded-2xl border border-gray-200 dark:border-gray-800 shadow-sm flex flex-col justify-center">
            <p className="text-xs text-gray-500 font-semibold uppercase tracking-wider mb-1 flex items-center gap-2">💰 BUDGET</p>
            <p className="text-sm font-semibold text-gray-900 dark:text-white">₹{tripData.budget_intelligence?.allocated_hotels_total_inr ? (tripData.budget_intelligence.allocated_hotels_total_inr + tripData.budget_intelligence.allocated_food_total_inr + tripData.budget_intelligence.allocated_activities_total_inr + tripData.budget_intelligence.allocated_transport_total_inr).toLocaleString() : 'Est.'}</p>
          </div>
          <div className="bg-white dark:bg-[#151923] p-5 rounded-2xl border border-gray-200 dark:border-gray-800 shadow-sm flex flex-col justify-center">
            <p className="text-xs text-gray-500 font-semibold uppercase tracking-wider mb-1 flex items-center gap-2">⛅ CLIMATE</p>
            <p className="text-sm font-semibold text-gray-900 dark:text-white">{tripData.weather_pipeline?.expected_condition || 'Standard'}</p>
          </div>
        </motion.div>

        {/* AI INSIGHT */}
        {tripData.ai_optimization_summary && (
          <motion.div variants={itemVariants} className="bg-white dark:bg-[#151923] rounded-3xl p-6 md:p-8 border border-gray-200 dark:border-gray-800 shadow-sm flex flex-col md:flex-row gap-6 items-start">
            <div className="w-12 h-12 rounded-full bg-indigo-50 dark:bg-indigo-900/30 flex items-center justify-center shrink-0">
              <span className="text-2xl">🧠</span>
            </div>
            <div>
              <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">AI insight</h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed text-sm">
                {tripData.ai_optimization_summary.join(' ')}
              </p>
            </div>
          </motion.div>
        )}

        {/* BUDGET BREAKDOWN */}
        <motion.div variants={itemVariants} className="pt-2">
          <div className="bg-white dark:bg-[#151923] rounded-3xl p-6 md:p-8 border border-gray-200 dark:border-gray-800 shadow-sm">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold flex items-center gap-2">
                <span>🪙</span> Budget breakdown <span className="bg-indigo-50 dark:bg-indigo-900/30 text-indigo-700 dark:text-[#8B9CFF] text-[10px] px-2 py-1 rounded-md font-semibold tracking-wider uppercase">Premium</span>
              </h2>
              {bIntell.remaining_buffer_inr < 0 ? (
                <span className="text-red-600 bg-red-50 dark:bg-red-900/20 px-3 py-1 rounded-full text-xs font-bold border border-red-100 dark:border-red-900/30">⚠️ Over budget by ₹{Math.abs(bIntell.remaining_buffer_inr).toLocaleString()}</span>
              ) : (
                <span className="text-green-600 bg-green-50 dark:bg-green-900/20 px-3 py-1 rounded-full text-xs font-bold border border-green-100 dark:border-green-900/30">✓ Under budget by ₹{(bIntell.remaining_buffer_inr || 0).toLocaleString()}</span>
              )}
            </div>
            
            <div className="mb-8">
              <h1 className="text-4xl font-bold mb-1 text-gray-900 dark:text-white">₹{totalAllocated.toLocaleString()} <span className="text-sm font-medium text-gray-500">of ₹{targetBudget > 0 ? targetBudget.toLocaleString() : (totalAllocated + 10000).toLocaleString()} limit</span></h1>
            </div>

            <div className="space-y-5 mb-8">
              {[
                { label: 'Stay', val: bIntell.allocated_hotels_total_inr, icon: '🏨', color: 'bg-indigo-500' },
                { label: 'Food', val: bIntell.allocated_food_total_inr, icon: '🍽️', color: 'bg-blue-500' },
                { label: 'Travel', val: bIntell.allocated_transport_total_inr, icon: '🚗', color: 'bg-teal-500' },
                { label: 'Activities', val: bIntell.allocated_activities_total_inr, icon: '🎯', color: 'bg-orange-500' },
              ].map((item, i) => (
                <motion.div 
                key={i} 
                className="mb-10 last:mb-0 relative"
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true, margin: "-50px" }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
              >
                  <div className="flex justify-between text-xs font-bold text-gray-700 dark:text-gray-300 mb-1.5">
                    <span className="flex items-center gap-2"><span>{item.icon}</span> {item.label}</span>
                    <span>₹{(item.val || 0).toLocaleString()}</span>
                  </div>
                  <div className="w-full h-2 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                    <motion.div 
                      initial={{ width: 0 }}
                      animate={{ width: `${Math.min(100, ((item.val || 0) / totalAllocated) * 100)}%` }}
                      transition={{ duration: 1, delay: 0.2 + i * 0.1 }}
                      className={`h-full ${item.color} rounded-full`}
                    />
                  </div>
                </motion.div>
              ))}
            </div>

            <div className="bg-green-50 dark:bg-green-900/10 rounded-2xl p-5 md:p-6 border border-green-100 dark:border-green-900/30">
              <h3 className="font-bold text-green-800 dark:text-green-400 mb-4 flex items-center gap-2"><span>✨</span> Lower-cost alternatives found</h3>
              <ul className="space-y-3 text-sm">
                <li className="flex justify-between items-center gap-4">
                  <span className="text-gray-700 dark:text-gray-300 leading-tight"><span className="font-semibold text-gray-900 dark:text-white">Stay:</span> Swap luxury resort for premium boutique hotel</span>
                  <span className="text-green-600 dark:text-green-400 font-bold shrink-0">-₹12,000</span>
                </li>
                <li className="flex justify-between items-center gap-4">
                  <span className="text-gray-700 dark:text-gray-300 leading-tight"><span className="font-semibold text-gray-900 dark:text-white">Travel:</span> Group taxi transfers instead of private SUV</span>
                  <span className="text-green-600 dark:text-green-400 font-bold shrink-0">-₹4,500</span>
                </li>
              </ul>
              <button className="w-full mt-5 bg-indigo-600 hover:bg-indigo-700 dark:bg-[#8B9CFF] dark:hover:bg-[#7A8CE6] dark:text-black text-white font-bold py-3.5 rounded-xl transition-colors shadow-sm flex items-center justify-center gap-2">
                🎛 Optimize for lower budget
              </button>
            </div>
          </div>
        </motion.div>

        {/* WEATHER PIPLENE */}
        {tripData.weather_pipeline && (
          <motion.div variants={itemVariants} className="pt-2">
            <div className="bg-gradient-to-br from-cyan-50 to-blue-50 dark:from-cyan-900/20 dark:to-blue-900/20 rounded-3xl p-6 md:p-8 border border-cyan-100 dark:border-cyan-900/30 shadow-sm flex flex-col md:flex-row gap-6 items-start">
              <div className="w-14 h-14 rounded-full bg-white dark:bg-[#151923] shadow-sm flex items-center justify-center shrink-0 text-3xl">
                ⛅
              </div>
              <div className="w-full">
                <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-1">Weather & Packing</h3>
                <p className="text-gray-600 dark:text-gray-300 text-sm mb-4 font-medium">
                  {tripData.weather_pipeline.expected_condition}
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="bg-white/60 dark:bg-[#151923]/60 rounded-xl p-4">
                    <h4 className="text-xs font-bold text-cyan-800 dark:text-cyan-400 uppercase tracking-wider mb-2">Packing Suggestions</h4>
                    <ul className="text-sm text-gray-700 dark:text-gray-300 space-y-1">
                      {tripData.weather_pipeline.packing_suggestions?.map((item: string, i: number) => (
                        <li key={i} className="flex items-center gap-2">
                          <span className="text-cyan-500">•</span> {item}
                        </li>
                      ))}
                    </ul>
                  </div>
                  {tripData.weather_pipeline.adaptive_itinerary_note && (
                    <div className="bg-white/60 dark:bg-[#151923]/60 rounded-xl p-4">
                      <h4 className="text-xs font-bold text-orange-800 dark:text-orange-400 uppercase tracking-wider mb-2">Agent Note</h4>
                      <p className="text-sm text-gray-700 dark:text-gray-300">{tripData.weather_pipeline.adaptive_itinerary_note}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* MASONRY ITINERARY */}
        <motion.div variants={itemVariants} className="pt-6">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2 mb-6">
            <span className="text-indigo-600 dark:text-[#8B9CFF]">⏱</span> Day-by-day itinerary
          </h2>
          
          <div className="columns-1 md:columns-2 lg:columns-3 gap-6 space-y-6">
            {itineraryDays.map((day: any, i: number) => (
              <div key={i} className="break-inside-avoid bg-white dark:bg-[#151923] rounded-3xl border border-gray-200 dark:border-gray-800 shadow-sm overflow-hidden flex flex-col">
                <div className="p-5 border-b border-gray-100 dark:border-gray-800/50">
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex gap-3">
                      <div className="bg-indigo-50 dark:bg-indigo-900/20 text-indigo-700 dark:text-indigo-400 font-bold rounded-xl w-12 h-12 flex items-center justify-center text-lg">
                        D{day.day_number}
                      </div>
                      <div className="pt-0.5">
                        <h3 className="font-bold text-gray-900 dark:text-white text-base leading-tight">{day.theme || 'Exploration'}</h3>
                        <p className="text-xs text-gray-500 mt-1">{day.date_string}</p>
                      </div>
                    </div>
                    {day.day_energy_badge && (
                      <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded-md ${
                        day.day_energy_badge.toLowerCase() === 'relaxed' ? 'text-green-700 bg-green-50 dark:bg-green-900/20' : 
                        day.day_energy_badge.toLowerCase() === 'active' ? 'text-orange-700 bg-orange-50 dark:bg-orange-900/20' : 
                        'text-indigo-700 bg-indigo-50 dark:bg-indigo-900/20'
                      }`}>✨ {day.day_energy_badge}</span>
                    )}
                  </div>
                  <div className="flex items-center gap-2 bg-gray-50 dark:bg-[#0B0F17] rounded-lg px-3 py-2 border border-gray-100 dark:border-gray-800">
                    <span className="text-sm">⛅</span>
                    <span className="text-xs font-medium text-gray-700 dark:text-gray-300">{day.weather_forecast || 'Sunny'}</span>
                  </div>
                </div>
                
                <div className="p-5 relative">
                  <div className="absolute left-[31px] top-6 bottom-6 w-0.5 bg-gray-100 dark:bg-gray-800 rounded-full"></div>
                  
                  <div className="space-y-6">
                    {Array.isArray(day.activities) && day.activities.map((act: any, idx: number) => (
                      <div key={idx} className="relative z-10 pl-12 group">
                        <div className="absolute left-[7px] top-1 w-2.5 h-2.5 rounded-full bg-indigo-500 border-[3px] border-white dark:border-[#151923] shadow-sm"></div>
                        <div className="flex justify-between items-baseline mb-1">
                          <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">{act.time_slot} {act.start_time && `• ${act.start_time}`}</p>
                          <p className="text-[10px] text-gray-500 font-medium">₹{act.estimated_cost_inr}</p>
                        </div>
                        <h4 className="font-bold text-gray-900 dark:text-white text-sm mb-1">{act.activity_name}</h4>
                        <p className="text-xs text-gray-600 dark:text-gray-400 leading-relaxed mb-2">{act.description}</p>
                        
                        {act.transit_estimate && (
                          <div className="flex items-center gap-2 mt-2 text-[10px] text-gray-500">
                            <span>🚗</span> <span>{act.transit_estimate}</span>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>



        {/* HOTELS ACCORDION */}
        <motion.div variants={itemVariants} className="pt-8">
          <button 
            onClick={() => setOpenSections(s => ({...s, hotels: !s.hotels}))}
            className="w-full flex justify-between items-center mb-4 group cursor-pointer"
          >
            <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
              <span>🏨</span> Hotel recommendations <span className="text-sm font-normal text-gray-400">{hotels.length} spots</span>
            </h2>
            <span className={`text-gray-400 transition-transform duration-300 text-xl ${openSections.hotels ? 'rotate-180' : ''}`}>⌃</span>
          </button>
          {openSections.hotels && (
            <div className="space-y-4">
              {hotels.map((hotel: any, i: number) => {
                const hotelImg = hotel.image_url && hotel.image_url.includes('unsplash') 
                  ? hotel.image_url 
                  : `https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&q=80&sig=${i}`;
                return (
                  <motion.div 
                    key={i}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.05 }}
                    className="group bg-white dark:bg-[#151923] rounded-2xl border border-gray-200 dark:border-gray-800 shadow-sm overflow-hidden flex hover:border-indigo-300 dark:hover:border-indigo-700 hover:shadow-md transition-all duration-300 cursor-pointer"
                  >
                    <div className="w-36 sm:w-48 shrink-0 bg-gray-100 dark:bg-gray-800 overflow-hidden relative">
                      <img src={hotelImg} alt={hotel.name} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                      <button className="absolute top-3 right-3 w-8 h-8 rounded-full bg-white/80 backdrop-blur-md flex items-center justify-center hover:bg-white transition shadow-sm">
                        <span className="text-sm">♡</span>
                      </button>
                    </div>
                    <div className="p-5 flex-1 flex flex-col justify-between min-w-0">
                      <div>
                        <div className="flex justify-between items-start gap-2 mb-1">
                          <h3 className="font-bold text-gray-900 dark:text-white text-base leading-tight truncate">{hotel.name}</h3>
                          <p className="font-bold text-gray-900 dark:text-white text-sm shrink-0">₹{hotel.price_per_night_inr?.toLocaleString()}</p>
                        </div>
                        <div className="flex items-center gap-2 text-xs text-gray-500 font-medium mb-3">
                          <span className="text-orange-500">{'★'.repeat(Math.round(hotel.rating))} {hotel.rating}</span> • <span>📍 {hotel.location_area}</span>
                        </div>
                        <div className="flex flex-wrap gap-1.5 mb-3">
                          {hotel.badges?.map((b: string, idx: number) => (
                            <span key={idx} className="text-[10px] bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 px-2.5 py-1 rounded-full font-semibold">{b}</span>
                          ))}
                          {hotel.amenities_tags?.slice(0, 3).map((a: string, idx: number) => (
                            <span key={`a-${idx}`} className="text-[10px] bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 px-2.5 py-1 rounded-full font-medium">{a}</span>
                          ))}
                        </div>
                      </div>
                      {hotel.explainability?.reason_why && (
                        <p className="text-xs text-gray-600 dark:text-gray-400 pt-3 border-t border-gray-100 dark:border-gray-800/50">
                          <span className="font-semibold text-indigo-600 dark:text-[#8B9CFF]">Why:</span> {hotel.explainability.reason_why}
                        </p>
                      )}
                    </div>
                  </motion.div>
                );
              })}
            </div>
          )}
        </motion.div>

        {/* FOOD ACCORDION */}
        <motion.div variants={itemVariants} className="pt-8">
          <button 
            onClick={() => setOpenSections(s => ({...s, food: !s.food}))}
            className="w-full flex justify-between items-center mb-4 group cursor-pointer"
          >
            <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
              <span>🍽️</span> Food recommendations <span className="text-sm font-normal text-gray-400">{foods.length} spots</span>
            </h2>
            <span className={`text-gray-400 transition-transform duration-300 text-xl ${openSections.food ? 'rotate-180' : ''}`}>⌃</span>
          </button>
          {openSections.food && (
            <div className="space-y-4">
              {foods.map((food: any, i: number) => {
                const foodImg = food.image_url && food.image_url.includes('unsplash')
                  ? food.image_url
                  : `https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=400&q=80&sig=${i}`;
                const displayName = food.restaurant_name || food.name || 'Restaurant';
                return (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.05 }}
                    className="group bg-white dark:bg-[#151923] rounded-2xl border border-gray-200 dark:border-gray-800 shadow-sm overflow-hidden flex hover:border-indigo-300 dark:hover:border-indigo-700 hover:shadow-md transition-all duration-300 cursor-pointer"
                  >
                    <div className="w-28 sm:w-36 shrink-0 bg-gray-100 dark:bg-gray-800 overflow-hidden relative">
                      <img src={foodImg} alt={displayName} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                    </div>
                    <div className="p-4 flex-1 min-w-0">
                      <h3 className="font-bold text-gray-900 dark:text-white text-sm mb-1.5 truncate">{displayName}</h3>
                      <div className="flex items-center gap-2 text-[10px] text-gray-500 font-medium mb-2 flex-wrap">
                        <span className={`px-2 py-0.5 rounded-md uppercase tracking-wider font-bold ${
                          food.dietary_suitability?.toLowerCase() === 'non-veg' ? 'bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400' : 
                          food.dietary_suitability?.toLowerCase() === 'veg' ? 'bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400' : 
                          'bg-orange-50 dark:bg-orange-900/20 text-orange-600 dark:text-orange-400'
                        }`}>
                          {food.dietary_suitability || 'Both'}
                        </span>
                        <span className="text-orange-500">{'★'.repeat(Math.round(food.rating || 4))} {food.rating}</span>
                        <span className="text-gray-400">{food.cuisine_type}</span>
                      </div>
                      <p className="text-[11px] text-gray-500 mb-2">📍 {food.distance}</p>
                      {food.explainability?.reason_why && (
                        <p className="text-xs text-gray-600 dark:text-gray-400 leading-relaxed">
                          <span className="font-semibold text-indigo-600 dark:text-[#8B9CFF]">Why:</span> {food.explainability.reason_why}
                        </p>
                      )}
                    </div>
                    <div className="flex items-center pr-4">
                      <button className="w-8 h-8 rounded-lg border border-gray-200 dark:border-gray-700 flex items-center justify-center text-gray-400 hover:text-indigo-600 transition">
                        <span className="text-sm">🔖</span>
                      </button>
                    </div>
                  </motion.div>
                );
              })}
            </div>
          )}
        </motion.div>

        {/* TRANSPORT ACCORDION */}
        {transports.length > 0 && (
          <motion.div variants={itemVariants} className="pt-8">
            <button 
              onClick={() => setOpenSections(s => ({...s, transport: !s.transport}))}
              className="w-full flex justify-between items-center mb-4 group cursor-pointer"
            >
              <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                <span>🚗</span> Transport recommendations <span className="text-sm font-normal text-gray-400">{transports.length} options</span>
              </h2>
              <span className={`text-gray-400 transition-transform duration-300 text-xl ${openSections.transport ? 'rotate-180' : ''}`}>⌃</span>
            </button>
            {openSections.transport && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {transports.map((t: any, i: number) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.08 }}
                    className="bg-white dark:bg-[#151923] rounded-2xl border border-gray-200 dark:border-gray-800 shadow-sm p-5 hover:border-teal-300 dark:hover:border-teal-700 hover:shadow-md transition-all duration-300"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-teal-50 dark:bg-teal-900/20 flex items-center justify-center text-xl">🚗</div>
                        <div>
                          <h3 className="font-bold text-gray-900 dark:text-white text-sm">{t.mode}</h3>
                          <p className="text-xs text-gray-500">{t.duration}</p>
                        </div>
                      </div>
                      <span className="text-sm font-bold text-teal-600 dark:text-teal-400">{t.cost_estimate}</span>
                    </div>
                    <div className="flex flex-wrap gap-1.5 mb-3">
                      {t.badges?.map((b: string, idx: number) => (
                        <span key={idx} className="text-[10px] bg-teal-50 dark:bg-teal-900/20 text-teal-600 dark:text-teal-400 px-2.5 py-1 rounded-full font-semibold">{b}</span>
                      ))}
                    </div>
                    {t.explainability?.reason_why && (
                      <p className="text-xs text-gray-600 dark:text-gray-400">
                        <span className="font-semibold text-teal-600 dark:text-teal-400">Why:</span> {t.explainability.reason_why}
                      </p>
                    )}
                  </motion.div>
                ))}
              </div>
            )}
          </motion.div>
        )}

        {/* ACTIVITIES ACCORDION */}
        {extraActivities.length > 0 && (
          <motion.div variants={itemVariants} className="pt-8">
            <button 
              onClick={() => setOpenSections(s => ({...s, activities: !s.activities}))}
              className="w-full flex justify-between items-center mb-4 group cursor-pointer"
            >
              <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                <span>🎯</span> Extra activities & hidden gems <span className="text-sm font-normal text-gray-400">{extraActivities.length} experiences</span>
              </h2>
              <span className={`text-gray-400 transition-transform duration-300 text-xl ${openSections.activities ? 'rotate-180' : ''}`}>⌃</span>
            </button>
            {openSections.activities && (
              <div className="space-y-4">
                {extraActivities.map((act: any, i: number) => {
                  const actImg = act.image_url && act.image_url.includes('unsplash')
                    ? act.image_url
                    : `https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=400&q=80&sig=${i}`;
                  return (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: i * 0.05 }}
                      className="group bg-white dark:bg-[#151923] rounded-2xl border border-gray-200 dark:border-gray-800 shadow-sm overflow-hidden flex hover:border-orange-300 dark:hover:border-orange-700 hover:shadow-md transition-all duration-300 cursor-pointer"
                    >
                      <div className="w-28 sm:w-36 shrink-0 bg-gray-100 dark:bg-gray-800 overflow-hidden relative">
                        <img src={actImg} alt={act.activity_name} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                      </div>
                      <div className="p-4 flex-1 min-w-0">
                        <h3 className="font-bold text-gray-900 dark:text-white text-sm mb-1.5 truncate">{act.activity_name}</h3>
                        <div className="flex items-center gap-2 text-[10px] text-gray-500 font-medium mb-2 flex-wrap">
                          <span className="bg-orange-50 dark:bg-orange-900/20 text-orange-600 dark:text-orange-400 px-2 py-0.5 rounded-md font-bold">{act.category || 'Experience'}</span>
                          <span className="text-orange-500">★ {act.rating}</span>
                          {act.duration && <span>⏱ {act.duration}</span>}
                          {act.best_time && <span>🌅 {act.best_time}</span>}
                        </div>
                        <div className="flex flex-wrap gap-1 mb-2">
                          {act.walking_effort && <span className="text-[9px] bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 px-2 py-0.5 rounded-full">{act.walking_effort}</span>}
                          {act.energy_level && <span className="text-[9px] bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 px-2 py-0.5 rounded-full">{act.energy_level}</span>}
                          {act.target_age_group && <span className="text-[9px] bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 px-2 py-0.5 rounded-full">{act.target_age_group}</span>}
                        </div>
                        {act.explainability?.reason_why && (
                          <p className="text-xs text-gray-600 dark:text-gray-400">
                            <span className="font-semibold text-orange-600 dark:text-orange-400">Why:</span> {act.explainability.reason_why}
                          </p>
                        )}
                      </div>
                      {act.estimated_cost_inr > 0 && (
                        <div className="flex items-center pr-4">
                          <span className="text-sm font-bold text-gray-700 dark:text-gray-300">₹{act.estimated_cost_inr?.toLocaleString()}</span>
                        </div>
                      )}
                    </motion.div>
                  );
                })}
              </div>
            )}
          </motion.div>
        )}

      </motion.main>
    </div>
  );
}