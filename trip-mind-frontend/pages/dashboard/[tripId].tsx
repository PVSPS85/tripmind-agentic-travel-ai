import React, { useState, useContext } from 'react';
import Head from 'next/head';
import { ThemeContext } from '../_app';

export default function Dashboard() {
  const [isOptimized, setIsOptimized] = useState(false);
  const { isDark, toggleTheme } = useContext(ThemeContext);

  // Function to trigger the native Save as PDF / Print dialog
  const handleExport = () => {
    window.print();
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-[#0B0F17] text-gray-900 dark:text-gray-100 pb-20 font-sans transition-colors duration-300">
      <Head>
        <title>Goa, India | TripMind AI</title>
      </Head>

      {/* Top Navigation */}
      <nav className="border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-[#0B0F17]/80 backdrop-blur-md sticky top-0 z-50 px-6 py-4 flex justify-between items-center transition-colors duration-300 print:hidden">
        <a href="/" className="flex items-center gap-2 font-display font-bold text-xl hover:opacity-80 transition-opacity">
          <span className="text-indigo-600 dark:text-[#8B9CFF]">TripMind</span> <span className="text-gray-900 dark:text-white">AI</span>
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

      <main className="max-w-[1400px] mx-auto px-6 pt-10">
        
        {/* Header */}
        <header className="flex flex-col md:flex-row justify-between items-start md:items-end mb-8 gap-4">
          <div>
            <p className="text-indigo-600 dark:text-[#8B9CFF] text-xs font-bold tracking-widest uppercase mb-2">Your Trip Plan</p>
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-2 transition-colors duration-300">Goa, India</h1>
            <p className="text-gray-600 dark:text-gray-400 transition-colors duration-300">7 days • 6 nights • Family</p>
          </div>
          <div className="flex gap-3 w-full md:w-auto print:hidden">
            <button 
              onClick={handleExport}
              className="flex-1 md:flex-none px-5 py-2.5 rounded-xl border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-[#151923] transition flex items-center justify-center gap-2 font-medium"
            >
              ↓ Export
            </button>
            <a href="/plan" className="flex-1 md:flex-none px-5 py-2.5 rounded-xl bg-indigo-600 dark:bg-[#8B9CFF] hover:bg-indigo-700 dark:hover:bg-[#7A8CE6] text-white dark:text-black transition flex items-center justify-center gap-2 font-semibold">
              ✨ New trip
            </a>
          </div>
        </header>

        {/* Quick Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: 'Dates', value: '15 Jun – 21 Jun, 2026', icon: '📅' },
            { label: 'Travelers', value: '2 Adults • 1 Kid • 1 Senior', icon: '👥' },
            { label: 'Budget', value: '₹1,40,000', icon: '💳' },
            { label: 'Climate', value: 'Monsoon onset • 26–31°C', icon: '☁️' }
          ].map((stat, i) => (
            <div key={i} className="bg-white dark:bg-[#151923] border border-gray-200 dark:border-gray-800 shadow-sm dark:shadow-none rounded-2xl p-4 transition-colors duration-300">
              <div className="flex items-center gap-2 text-xs font-semibold text-gray-500 dark:text-gray-400 tracking-wider uppercase mb-2">
                <span>{stat.icon}</span> {stat.label}
              </div>
              <div className="font-medium text-gray-900 dark:text-white transition-colors duration-300">{stat.value}</div>
            </div>
          ))}
        </div>

        {/* AI Insight */}
        <div className="bg-white dark:bg-[#151923] border border-gray-200 dark:border-gray-800 shadow-sm dark:shadow-none rounded-2xl p-6 mb-12 relative overflow-hidden transition-colors duration-300">
          <div className="absolute top-0 left-0 w-1 h-full bg-indigo-500 dark:bg-[#8B9CFF]"></div>
          <div className="flex items-center gap-2 text-indigo-600 dark:text-[#8B9CFF] font-semibold mb-3">
            <span>🧠</span> AI insight
          </div>
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed text-sm md:text-base transition-colors duration-300">
            We balanced this week for a multi-generational group — gentle mornings for your senior traveler, mid-day pool and beach time for the kid, and unhurried evenings for the adults. Goa in mid-June is the start of the monsoon, so we placed outdoor excursions early in the day and reserved spice plantations, museums, and covered markets for the showers. Every restaurant and stay is chosen for accessibility, family comfort, and proven hospitality.
          </p>
        </div>

        {/* Main Content Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
          
          {/* LEFT COLUMN (Wider) */}
          <div className="lg:col-span-2 space-y-12">
            
            {/* 1. Day-by-Day Itinerary */}
            <section>
              <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2 transition-colors duration-300">
                <span className="text-indigo-600 dark:text-[#8B9CFF]">⏱</span> Day-by-day itinerary
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                
                {/* D1 */}
                <div className="bg-white dark:bg-[#151923] border border-gray-200 dark:border-gray-800 shadow-sm dark:shadow-none rounded-2xl p-5 flex flex-col transition-colors duration-300">
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex gap-3">
                      <div className="bg-indigo-50 dark:bg-[#1A1F2E] text-indigo-600 dark:text-[#8B9CFF] font-bold rounded-lg w-10 h-10 flex items-center justify-center border border-indigo-100 dark:border-gray-700 shrink-0">D1</div>
                      <div>
                        <h3 className="font-bold text-gray-900 dark:text-white text-sm leading-tight">Arrival & North Goa <br/> welcome</h3>
                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Settle in</p>
                      </div>
                    </div>
                    <span className="bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 px-2.5 py-1 rounded-md text-[10px] font-medium border border-green-200 dark:border-green-800/50 flex items-center gap-1">⚡ Relaxed</span>
                  </div>
                  <div className="bg-gray-50 dark:bg-[#0B0F17] rounded-xl p-3 flex justify-between items-center border border-gray-200 dark:border-gray-800 mb-4 text-sm transition-colors duration-300">
                    <span className="text-yellow-600 dark:text-yellow-500 flex items-center gap-2">☀️ Sunny</span>
                    <span className="text-gray-600 dark:text-gray-400">31°C</span>
                  </div>

                  <div className="space-y-1">
                     <p className="text-[10px] font-bold tracking-widest text-gray-500 uppercase mb-3 flex items-center gap-2"><span>☼</span> AFTERNOON</p>
                     <div className="flex gap-3 mb-4">
                       <div className="w-10 text-xs text-gray-500 dark:text-gray-400 font-mono pt-0.5 shrink-0">14:00</div>
                       <div className="flex-1">
                         <div className="flex justify-between items-start">
                            <h4 className="font-semibold text-gray-900 dark:text-white text-sm leading-tight">Check in at Taj Holiday Village</h4>
                            <span className="w-1.5 h-1.5 rounded-full bg-indigo-500 dark:bg-[#8B9CFF] shrink-0 mt-1.5"></span>
                         </div>
                         <p className="text-xs text-gray-600 dark:text-gray-400 mt-1 leading-relaxed">Step-free villa access; easy for your senior traveler</p>
                       </div>
                     </div>

                     <p className="text-[10px] font-bold tracking-widest text-gray-500 uppercase mt-5 mb-3 flex items-center gap-2"><span>☽</span> EVENING</p>
                     <div className="flex gap-2 text-xs text-gray-500 items-center pl-[52px] mb-3"><span className="text-[10px]">🚶</span> 8 min · Free</div>
                     <div className="flex gap-3 mb-4">
                       <div className="w-10 text-xs text-gray-500 dark:text-gray-400 font-mono pt-0.5 shrink-0">17:00</div>
                       <div className="flex-1">
                         <div className="flex justify-between items-start">
                            <h4 className="font-semibold text-gray-900 dark:text-white text-sm leading-tight">Sunset walk at Candolim Beach</h4>
                            <span className="w-1.5 h-1.5 rounded-full bg-teal-500 dark:bg-teal-400 shrink-0 mt-1.5"></span>
                         </div>
                         <p className="text-xs text-gray-600 dark:text-gray-400 mt-1 leading-relaxed">Quiet stretch, gentle pace, near resort</p>
                       </div>
                     </div>

                     <div className="flex gap-2 text-xs text-gray-500 items-center pl-[52px] mb-3"><span className="text-[10px]">🚗</span> 12 min · ₹160</div>
                     <div className="flex gap-3 mb-2">
                       <div className="w-10 text-xs text-gray-500 dark:text-gray-400 font-mono pt-0.5 shrink-0">20:00</div>
                       <div className="flex-1">
                         <div className="flex justify-between items-start">
                            <h4 className="font-semibold text-gray-900 dark:text-white text-sm leading-tight">Welcome dinner at Fisherman's Wharf</h4>
                            <span className="w-1.5 h-1.5 rounded-full bg-orange-500 dark:bg-orange-400 shrink-0 mt-1.5"></span>
                         </div>
                         <p className="text-xs text-gray-600 dark:text-gray-400 mt-1 leading-relaxed">Kid-friendly riverside menu, live music</p>
                       </div>
                     </div>
                  </div>
                </div>

                {/* D2 */}
                <div className="bg-white dark:bg-[#151923] border border-gray-200 dark:border-gray-800 shadow-sm dark:shadow-none rounded-2xl p-5 flex flex-col transition-colors duration-300">
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex gap-3">
                      <div className="bg-indigo-50 dark:bg-[#1A1F2E] text-indigo-600 dark:text-[#8B9CFF] font-bold rounded-lg w-10 h-10 flex items-center justify-center border border-indigo-100 dark:border-gray-700 shrink-0">D2</div>
                      <div>
                        <h3 className="font-bold text-gray-900 dark:text-white text-sm leading-tight">Old Goa heritage</h3>
                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Culture</p>
                      </div>
                    </div>
                    <span className="bg-blue-100 dark:bg-indigo-900/30 text-blue-700 dark:text-indigo-400 px-2.5 py-1 rounded-md text-[10px] font-medium border border-blue-200 dark:border-indigo-800/50 flex items-center gap-1">⚡ Balanced</span>
                  </div>
                  <div className="bg-gray-50 dark:bg-[#0B0F17] rounded-xl p-3 flex justify-between items-center border border-gray-200 dark:border-gray-800 mb-4 text-sm transition-colors duration-300">
                    <span className="text-gray-600 dark:text-gray-300 flex items-center gap-2">⛅ Partly cloudy</span>
                    <span className="text-gray-600 dark:text-gray-400">29°C</span>
                  </div>

                  <div className="space-y-1">
                     <p className="text-[10px] font-bold tracking-widest text-gray-500 uppercase mb-3 flex items-center gap-2"><span>☼</span> MORNING</p>
                     <div className="flex gap-3 mb-4">
                       <div className="w-10 text-xs text-gray-500 dark:text-gray-400 font-mono pt-0.5 shrink-0">09:30</div>
                       <div className="flex-1">
                         <div className="flex justify-between items-start">
                            <h4 className="font-semibold text-gray-900 dark:text-white text-sm leading-tight">Basilica of Bom Jesus & Sé Cathedral</h4>
                            <span className="w-1.5 h-1.5 rounded-full bg-pink-500 shrink-0 mt-1.5"></span>
                         </div>
                         <p className="text-xs text-gray-600 dark:text-gray-400 mt-1 leading-relaxed">Cooler hours, fewer crowds, paired sites</p>
                       </div>
                     </div>

                     <p className="text-[10px] font-bold tracking-widest text-gray-500 uppercase mt-5 mb-3 flex items-center gap-2"><span>☼</span> AFTERNOON</p>
                     <div className="flex gap-2 text-xs text-gray-500 items-center pl-[52px] mb-3"><span className="text-[10px]">🚗</span> 18 min · ₹240</div>
                     <div className="flex gap-3 mb-4">
                       <div className="w-10 text-xs text-gray-500 dark:text-gray-400 font-mono pt-0.5 shrink-0">12:30</div>
                       <div className="flex-1">
                         <div className="flex justify-between items-start">
                            <h4 className="font-semibold text-gray-900 dark:text-white text-sm leading-tight">Lunch at Viva Panjim</h4>
                            <span className="w-1.5 h-1.5 rounded-full bg-orange-500 dark:bg-orange-400 shrink-0 mt-1.5"></span>
                         </div>
                         <p className="text-xs text-gray-600 dark:text-gray-400 mt-1 leading-relaxed">On-route to next stop, authentic Goan home cooking</p>
                       </div>
                     </div>

                     <div className="flex gap-2 text-xs text-gray-500 items-center pl-[52px] mb-3"><span className="text-[10px]">🚶</span> 3 min · Free</div>
                     <div className="flex gap-3 mb-4">
                       <div className="w-10 text-xs text-gray-500 dark:text-gray-400 font-mono pt-0.5 shrink-0">15:30</div>
                       <div className="flex-1">
                         <div className="flex justify-between items-start">
                            <h4 className="font-semibold text-gray-900 dark:text-white text-sm leading-tight">Latin Quarter walking tour</h4>
                            <span className="w-1.5 h-1.5 rounded-full bg-pink-500 shrink-0 mt-1.5"></span>
                         </div>
                         <p className="text-xs text-gray-600 dark:text-gray-400 mt-1 leading-relaxed">Same neighborhood — no extra transit</p>
                       </div>
                     </div>
                  </div>
                </div>

                {/* D3 */}
                <div className="bg-white dark:bg-[#151923] border border-gray-200 dark:border-gray-800 shadow-sm dark:shadow-none rounded-2xl p-5 flex flex-col transition-colors duration-300">
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex gap-3">
                      <div className="bg-indigo-50 dark:bg-[#1A1F2E] text-indigo-600 dark:text-[#8B9CFF] font-bold rounded-lg w-10 h-10 flex items-center justify-center border border-indigo-100 dark:border-gray-700 shrink-0">D3</div>
                      <div>
                        <h3 className="font-bold text-gray-900 dark:text-white text-sm leading-tight">Spice plantation & <br/> countryside</h3>
                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Nature</p>
                      </div>
                    </div>
                    <span className="bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-500 px-2.5 py-1 rounded-md text-[10px] font-medium border border-yellow-200 dark:border-yellow-800/50 flex items-center gap-1">⚡ Active</span>
                  </div>
                  <div className="bg-gray-50 dark:bg-[#0B0F17] rounded-xl p-3 flex justify-between items-center border border-gray-200 dark:border-gray-800 mb-4 text-sm transition-colors duration-300">
                    <span className="text-green-600 dark:text-green-400 flex items-center gap-2">🌧️ Light rain</span>
                    <span className="text-gray-600 dark:text-gray-400">26°C</span>
                  </div>

                  <div className="bg-indigo-50 dark:bg-[#1A1F2E] p-3 rounded-xl border border-indigo-100 dark:border-[#8B9CFF]/20 mb-5 transition-colors duration-300">
                     <p className="text-xs text-indigo-700 dark:text-[#8B9CFF]">✨ Indoor backup added — Goa State Museum in the afternoon if showers persist.</p>
                  </div>

                  <div className="space-y-1">
                     <p className="text-[10px] font-bold tracking-widest text-gray-500 uppercase mb-3 flex items-center gap-2"><span>☼</span> MORNING</p>
                     <div className="flex gap-2 text-xs text-gray-500 items-center pl-[52px] mb-3"><span className="text-[10px]">🚗</span> 55 min · ₹950</div>
                     <div className="flex gap-3 mb-4">
                       <div className="w-10 text-xs text-gray-500 dark:text-gray-400 font-mono pt-0.5 shrink-0">09:00</div>
                       <div className="flex-1">
                         <div className="flex justify-between items-start">
                            <h4 className="font-semibold text-gray-900 dark:text-white text-sm leading-tight">Sahakari Spice Farm tour & lunch</h4>
                            <span className="w-1.5 h-1.5 rounded-full bg-green-500 shrink-0 mt-1.5"></span>
                         </div>
                         <p className="text-xs text-gray-600 dark:text-gray-400 mt-1 leading-relaxed">Covered walkways — rain-safe</p>
                       </div>
                     </div>
                  </div>
                </div>

              </div>
            </section>

            {/* 2. Hotel Recommendations */}
            <section>
              <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6 flex items-center justify-between transition-colors duration-300">
                <span className="flex items-center gap-2"><span className="text-indigo-600 dark:text-[#8B9CFF]">🏨</span> Hotel recommendations</span>
              </h2>
              <div className="space-y-4">
                {[
                  { name: "Park Hyatt Goa Resort and Spa", price: "₹18,200", rating: "4.8", loc: "Cavelossim", tags: ["Luxury", "Senior-friendly"], desc: "Sprawling Indo-Portuguese estate with seven pools, a renowned Sereno spa, and step-free villa access. Excellent for the slow second half of the trip." },
                  { name: "Taj Holiday Village Resort & Spa", price: "₹14,500", rating: "4.7", loc: "Sinquerim", tags: ["Family-friendly", "Highly rated"], desc: "Cottage-style rooms set in 28 acres of palm groves — easy for seniors to navigate, with a shallow kids' pool and a private beach gate." },
                  { name: "Novotel Goa Candolim", price: "₹9,800", rating: "4.5", loc: "Candolim", tags: ["Budget", "Near center"], desc: "Best value-for-money pick in North Goa with a Kids' Club, generous breakfast buffet, and a 5-minute walk to Candolim Beach. Smart fallback if you trim spend." }
                ].map((hotel, i) => (
                  <div key={i} className={`bg-white dark:bg-[#151923] border ${isOptimized && i === 2 ? 'border-green-500 shadow-[0_0_15px_rgba(34,197,94,0.1)]' : 'border-gray-200 dark:border-gray-800'} rounded-2xl p-5 flex gap-4 transition-colors duration-300`}>
                    <div className="w-24 h-24 md:w-32 md:h-32 bg-gray-200 dark:bg-gray-800 rounded-xl overflow-hidden shrink-0 transition-colors duration-300"></div>
                    <div className="flex-1 flex flex-col justify-between">
                      <div>
                        <div className="flex justify-between items-start">
                          <h3 className="font-bold text-gray-900 dark:text-white transition-colors duration-300">{hotel.name}</h3>
                          <span className="font-bold text-gray-900 dark:text-white text-right shrink-0 transition-colors duration-300">{hotel.price} <span className="text-xs text-gray-500 font-normal">/ night</span></span>
                        </div>
                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">⭐ {hotel.rating} • {hotel.loc}, Goa</p>
                      </div>
                      <div>
                        <div className="flex gap-2 mt-2 mb-2">
                          {hotel.tags.map(t => <span key={t} className="bg-indigo-50 dark:bg-[#1A1F2E] text-indigo-700 dark:text-[#8B9CFF] px-2 py-1 rounded text-[10px] border border-indigo-100 dark:border-[#8B9CFF]/20 transition-colors duration-300">{t}</span>)}
                        </div>
                        <p className="text-xs text-gray-600 dark:text-gray-300 transition-colors duration-300"><span className="font-bold text-indigo-600 dark:text-[#8B9CFF]">Why:</span> {hotel.desc}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {/* 3. Food Recommendations */}
            <section>
              <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2 transition-colors duration-300">
                <span className="text-indigo-600 dark:text-[#8B9CFF]">🍽️</span> Food recommendations
              </h2>
              <div className="space-y-4">
                {[
                  { name: "Mum's Kitchen", type: "Both", rating: "4.6", loc: "Panjim - 8 km from hotel", desc: "Family-run institution preserving home-style Goan recipes — Sorpotel, Xacuti, and a beautifully spiced fish curry. Has both veg and non-veg thalis." },
                  { name: "Fisherman's Wharf", type: "Non-Veg", rating: "4.5", loc: "Cavelossim • riverside", desc: "Open-air riverside dining with live music. Their butter-garlic prawns and Goan fish curry are crowd-pleasers — easy menu for kids too." },
                  { name: "Viva Panjim", type: "Both", rating: "4.5", loc: "Fontainhas • 9 km", desc: "Tucked inside the Latin Quarter, this small heritage home serves authentic Chicken Cafreal and Prawn Balchao at modest prices. Lovely lunch stop." },
                  { name: "Vinayak Family Restaurant", type: "Veg friendly", rating: "4.4", loc: "Assagao • 14 km", desc: "A staple for Goan thali. Excellent veg and non-veg options in a casual setting." }
                ].map((food, i) => (
                  <div key={i} className="bg-white dark:bg-[#151923] border border-gray-200 dark:border-gray-800 shadow-sm dark:shadow-none rounded-2xl p-4 flex gap-4 transition-colors duration-300">
                    <div className="w-20 h-20 bg-gray-200 dark:bg-gray-800 rounded-xl overflow-hidden shrink-0 transition-colors duration-300"></div>
                    <div>
                      <h3 className="font-bold text-gray-900 dark:text-white text-sm transition-colors duration-300">{food.name}</h3>
                      <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400 mt-1">
                        <span className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${food.type === 'Non-Veg' ? 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400' : 'bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400'}`}>{food.type}</span>
                        <span>⭐ {food.rating} • {food.loc}</span>
                      </div>
                      <p className="text-xs text-gray-600 dark:text-gray-300 mt-2 transition-colors duration-300"><span className="font-bold text-indigo-600 dark:text-[#8B9CFF]">Why:</span> {food.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {/* 4. Transport Recommendations */}
            <section>
              <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2 transition-colors duration-300">
                <span className="text-indigo-600 dark:text-[#8B9CFF]">🚗</span> Transport recommendations
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[
                  { title: "Pre-booked AC cab", price: "₹2,800 / day", tag: "Best comfort", desc: "Recommended for daily outings during monsoon — door-to-door pickup, AC, and trunk space for strollers." },
                  { title: "Auto rickshaw", price: "₹80-₹250", tag: "Quick hops", desc: "Best for short transfers within North Goa beaches and Panjim lanes when it isn't raining." },
                  { title: "Rented scooter", price: "₹400 / day", tag: "Independent", desc: "Optional for the two adults on dry afternoons — skip during showers and with the senior traveler aboard." },
                  { title: "Walking on-site", price: "Free", tag: "Resort & old town", desc: "Most resort, beach, and Latin Quarter stops are within an easy walk — no transit needed." }
                ].map((trans, i) => (
                  <div key={i} className="bg-white dark:bg-[#151923] border border-gray-200 dark:border-gray-800 shadow-sm dark:shadow-none rounded-2xl p-5 transition-colors duration-300">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-bold text-gray-900 dark:text-white transition-colors duration-300">{trans.title}</h3>
                      <span className="text-[10px] font-medium bg-teal-100 dark:bg-teal-900/30 text-teal-700 dark:text-teal-400 px-2 py-1 rounded">{trans.tag}</span>
                    </div>
                    <p className="text-xs text-gray-500 dark:text-gray-400 font-mono mb-3">{trans.price}</p>
                    <p className="text-xs text-gray-600 dark:text-gray-300 transition-colors duration-300"><span className="font-bold text-indigo-600 dark:text-[#8B9CFF]">Why:</span> {trans.desc}</p>
                  </div>
                ))}
              </div>
            </section>

            {/* 5. Extra activity add-ons */}
            <section>
              <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2 transition-colors duration-300">
                <span className="text-indigo-600 dark:text-[#8B9CFF]">✨</span> Extra activity add-ons
              </h2>
              <div className="bg-teal-50 dark:bg-[#1A1F2E] border border-teal-200 dark:border-teal-900/50 rounded-xl p-4 mb-4 transition-colors duration-300">
                <p className="text-xs text-teal-700 dark:text-teal-400 font-medium">⚡ None of these repeat your itinerary. These are optional add-ons — nearby experiences, rainy-day fallbacks, and adult-only detours you can slot in based on your group's energy and weather on the day.</p>
              </div>
              <div className="space-y-4">
                {[
                  { name: "Chapora Fort at sunrise", time: "Morning", rating: "4.5", type: "Heritage • Fort" },
                  { name: "Anjuna Flea Market", time: "Afternoon", rating: "4.4", type: "Shopping & culture" },
                  { name: "Goa Science Centre, Panjim", time: "Morning", rating: "4.3", type: "Kids • Indoor" },
                  { name: "Butterfly Conservatory of Goa", time: "Morning", rating: "4.6", type: "Nature • Wildlife" }
                ].map((act, i) => (
                  <div key={i} className="bg-white dark:bg-[#151923] border border-gray-200 dark:border-gray-800 shadow-sm dark:shadow-none rounded-2xl p-4 flex gap-4 items-center transition-colors duration-300">
                     <div className="w-16 h-16 bg-gray-200 dark:bg-gray-800 rounded-xl overflow-hidden shrink-0 relative transition-colors duration-300">
                        <span className="absolute top-1 left-1 bg-black/70 text-white text-[8px] px-1.5 py-0.5 rounded">{act.time}</span>
                     </div>
                     <div>
                        <h3 className="font-bold text-gray-900 dark:text-white text-sm transition-colors duration-300">{act.name}</h3>
                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">⭐ {act.rating} • {act.type}</p>
                     </div>
                  </div>
                ))}
              </div>
            </section>
          </div>

          {/* RIGHT COLUMN (Sticky Sidebar) */}
          <div className="space-y-6 lg:sticky lg:top-24">
            
            {/* Budget Breakdown */}
            <div className="bg-white dark:bg-[#151923] border border-gray-200 dark:border-gray-800 shadow-sm dark:shadow-none rounded-2xl p-6 transition-colors duration-300">
              <div className="flex justify-between items-center mb-6">
                <h3 className="font-bold text-gray-900 dark:text-white flex items-center gap-2 transition-colors duration-300">
                  <span className="text-indigo-600 dark:text-[#8B9CFF]">💳</span> Budget breakdown
                </h3>
                {isOptimized ? (
                  <span className="bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 px-2 py-1 rounded-md text-[10px] font-bold border border-green-200 dark:border-green-800/50 transition-colors duration-300">✓ Under budget</span>
                ) : (
                  <span className="bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 px-2 py-1 rounded-md text-[10px] font-bold border border-red-200 dark:border-red-800/50 transition-colors duration-300">⚠️ Over by ₹22,000</span>
                )}
              </div>
              
              <div className="mb-6">
                <div className="text-3xl font-bold text-gray-900 dark:text-white mb-1 transition-colors duration-300">
                  {isOptimized ? '₹1,36,700' : '₹1,62,000'}
                </div>
                <div className="text-sm text-gray-500 dark:text-gray-400">of ₹1,40,000 budget</div>
              </div>

              <div className="space-y-4 mb-6">
                {[
                  { label: 'Stay', value: isOptimized ? '₹69,200' : '₹88,000', width: isOptimized ? 'w-[75%]' : 'w-full' },
                  { label: 'Food', value: '₹24,500', width: 'w-[40%]' },
                  { label: 'Travel', value: isOptimized ? '₹21,500' : '₹28,000', width: isOptimized ? 'w-[20%]' : 'w-[30%]' },
                  { label: 'Activities', value: '₹21,500', width: 'w-[25%]' },
                ].map((item, i) => (
                  <div key={i}>
                    <div className="flex justify-between text-sm text-gray-600 dark:text-gray-300 mb-1.5 transition-colors duration-300">
                      <span>{item.label}</span>
                      <span className="font-mono text-gray-900 dark:text-gray-400">{item.value}</span>
                    </div>
                    <div className="h-1.5 w-full bg-gray-100 dark:bg-[#0B0F17] rounded-full overflow-hidden transition-colors duration-300">
                      <div className={`h-full transition-all duration-500 bg-indigo-500 dark:bg-[#8B9CFF] rounded-full ${item.width}`}></div>
                    </div>
                  </div>
                ))}
              </div>

              {!isOptimized && (
                <div className="mb-5 bg-gray-50 dark:bg-[#1A1F2E] p-4 rounded-xl border border-gray-200 dark:border-gray-700 text-xs text-gray-700 dark:text-gray-300 space-y-2 transition-colors duration-300">
                   <p className="font-semibold text-indigo-600 dark:text-[#8B9CFF] mb-3 flex items-center gap-1">✨ Lower-cost alternatives</p>
                   <div className="flex justify-between items-center">
                     <span>Stay: Park Hyatt → Novotel</span> 
                     <span className="text-green-600 dark:text-green-400 font-mono">-₹18,800</span>
                   </div>
                   <div className="flex justify-between items-center">
                     <span>Travel: SUV → Shared cab</span> 
                     <span className="text-green-600 dark:text-green-400 font-mono">-₹6,500</span>
                   </div>
                </div>
              )}

              <button 
                onClick={() => setIsOptimized(!isOptimized)}
                className="w-full bg-indigo-50 dark:bg-[#8B9CFF]/10 hover:bg-indigo-100 dark:hover:bg-[#8B9CFF]/20 text-indigo-700 dark:text-[#8B9CFF] font-medium py-3 rounded-xl border border-indigo-200 dark:border-[#8B9CFF]/30 transition-colors text-sm"
              >
                {isOptimized ? '↺ Revert to premium' : '⚡ Optimize for lower budget'}
              </button>
            </div>

            {/* Packing Essentials */}
            <div className="bg-white dark:bg-[#151923] border border-gray-200 dark:border-gray-800 shadow-sm dark:shadow-none rounded-2xl p-6 transition-colors duration-300">
              <h3 className="font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2 transition-colors duration-300">
                <span className="text-indigo-600 dark:text-[#8B9CFF]">🛡️</span> Packing essentials
              </h3>
              <ul className="space-y-3">
                {[
                  'Light raincoat or compact umbrella for monsoon showers',
                  'Quick-dry sandals and waterproof footwear for wet sand',
                  'SPF 50+ sunscreen — UV is moderate but persistent',
                  'Mosquito repellent for evenings, especially inland',
                  'Modest cover-up for church visits in Old Goa',
                  'Power bank and zip-lock pouches for electronics in rain',
                  'Senior comfort kit: regular medications, reading glasses, light shawl for AC',
                  'Cash in INR for local markets and small eateries'
                ].map((item, i) => (
                  <li key={i} className="flex gap-3 text-sm text-gray-600 dark:text-gray-300 items-start transition-colors duration-300">
                    <span className="text-green-500 dark:text-green-400 mt-0.5">✓</span>
                    <span className="leading-relaxed">{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            <a href="/plan" className="block text-center w-full bg-transparent hover:bg-gray-100 dark:hover:bg-white/5 text-gray-600 dark:text-gray-300 font-medium py-3 rounded-xl border border-gray-300 dark:border-gray-700 transition-colors text-sm print:hidden">
              ♡ Plan another trip
            </a>

          </div>
        </div>
      </main>
    </div>
  );
}