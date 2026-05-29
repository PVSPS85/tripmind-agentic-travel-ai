import React, { useContext } from 'react';
import Head from 'next/head';
import { ThemeContext } from './_app';
import { motion } from 'framer-motion';

const features = [
  {
    icon: '🧠',
    title: 'Multi-Agent AI',
    description: 'Seven specialized AI agents collaborate to analyze demographics, weather, attractions, dining, and transport.'
  },
  {
    icon: '👨‍👩‍👧‍👦',
    title: 'Group-Aware Planning',
    description: 'Adapts pacing, accessibility, and energy levels for kids, adults, and seniors traveling together.'
  },
  {
    icon: '💰',
    title: 'Smart Budget Engine',
    description: 'Automatically allocates your budget across stays, food, travel, and activities with a safety buffer.'
  },
  {
    icon: '⛅',
    title: 'Weather Adaptive',
    description: 'Pulls real-time forecasts and swaps outdoor plans for indoor alternatives when rain is expected.'
  },
  {
    icon: '🗺️',
    title: 'Day-by-Day Itinerary',
    description: 'Morning, afternoon, and evening slots organized geographically with transit estimates between stops.'
  },
  {
    icon: '✨',
    title: 'Explainable AI',
    description: 'Every recommendation comes with a "Why this place?" explanation so you understand the reasoning.'
  },
];

const destinations = [
  { name: 'Goa', emoji: '🏖️', color: 'from-orange-400 to-pink-500' },
  { name: 'Manali', emoji: '🏔️', color: 'from-cyan-400 to-blue-500' },
  { name: 'Jaipur', emoji: '🏛️', color: 'from-amber-400 to-orange-500' },
  { name: 'Ooty', emoji: '🌿', color: 'from-green-400 to-emerald-500' },
  { name: 'Bengaluru', emoji: '💻', color: 'from-violet-400 to-purple-500' },
  { name: 'Kochi', emoji: '🚢', color: 'from-teal-400 to-cyan-500' },
];

export default function Home() {
  const { isDark, toggleTheme } = useContext(ThemeContext);

  return (
    <div className="min-h-screen text-gray-900 dark:text-gray-100 font-sans flex flex-col overflow-hidden">
      <Head>
        <title>TripMind AI — Plan Thoughtful Group Trips, Guided by AI</title>
        <meta name="description" content="TripMind AI uses multiple specialized AI agents to plan perfect group trips with smart budgets, weather-adaptive itineraries, and explainable recommendations." />
      </Head>

      {/* Navigation */}
      <nav className="border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-[#0B0F17]/80 backdrop-blur-xl sticky top-0 z-50 px-6 py-4 flex justify-between items-center transition-colors duration-300">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white text-sm font-bold shadow-lg shadow-indigo-500/20">
            TM
          </div>
          <span className="font-bold text-xl">
            <span className="text-[#8B9CFF]">TripMind</span>{' '}
            <span className="text-gray-900 dark:text-white">AI</span>
          </span>
        </div>
        <div className="flex items-center gap-4 text-sm">
          <span className="hidden sm:flex items-center gap-2 text-gray-500 dark:text-gray-400">
            <span className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]"></span> Agents online
          </span>
          <button onClick={toggleTheme} className="w-8 h-8 flex items-center justify-center rounded-lg border border-gray-300 dark:border-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-[#1A1F2E] transition-colors">
            {isDark ? '☼' : '☾'}
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="flex-grow relative">
        {/* Animated background elements */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-20 left-1/4 w-96 h-96 bg-indigo-500/5 dark:bg-indigo-500/10 rounded-full blur-[120px]"></div>
          <div className="absolute bottom-20 right-1/4 w-80 h-80 bg-purple-500/5 dark:bg-purple-500/8 rounded-full blur-[100px]"></div>
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-[#8B9CFF]/3 rounded-full blur-[150px]"></div>
        </div>

        {/* Hero Content */}
        <div className="relative z-10 max-w-5xl mx-auto px-6 pt-20 pb-16 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="inline-flex items-center gap-2 bg-indigo-50 dark:bg-indigo-900/20 text-indigo-700 dark:text-indigo-300 text-xs font-bold tracking-widest uppercase px-4 py-2 rounded-full mb-8 border border-indigo-100 dark:border-indigo-800/30">
              <span className="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-pulse"></span>
              Powered by 7 AI Agents
            </div>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-5xl sm:text-6xl md:text-7xl font-extrabold leading-[1.1] mb-6"
          >
            Plan thoughtful group trips,{' '}
            <br className="hidden sm:block" />
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-[#8B9CFF] via-indigo-400 to-purple-500">
              guided by AI.
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-lg sm:text-xl text-gray-500 dark:text-gray-400 max-w-2xl mx-auto mb-10 leading-relaxed"
          >
            Tell us your destination, group, and budget. TripMind&apos;s multi-agent system
            crafts a weather-aware, budget-optimized itinerary with explainable recommendations.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center"
          >
            <a
              href="/plan"
              className="group px-8 py-4 bg-gradient-to-r from-[#8B9CFF] to-indigo-500 text-white font-bold rounded-2xl text-lg transition-all duration-300 shadow-[0_4px_24px_rgba(139,156,255,0.3)] hover:shadow-[0_8px_32px_rgba(139,156,255,0.5)] hover:scale-[1.02] flex items-center gap-2"
            >
              ✨ Plan my trip
              <span className="group-hover:translate-x-1 transition-transform">→</span>
            </a>
          </motion.div>

          {/* Destination pills */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
            className="mt-16 flex flex-wrap justify-center gap-3"
          >
            {destinations.map((dest) => (
              <a
                key={dest.name}
                href={`/plan?dest=${encodeURIComponent(dest.name + ', India')}`}
                className="group inline-flex items-center gap-2 px-4 py-2.5 rounded-full bg-white dark:bg-[#151923] border border-gray-200 dark:border-gray-800 hover:border-[#8B9CFF] dark:hover:border-[#8B9CFF]/50 transition-all duration-300 hover:shadow-md"
              >
                <span className={`w-6 h-6 rounded-full bg-gradient-to-r ${dest.color} flex items-center justify-center text-xs`}>
                  {dest.emoji}
                </span>
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300 group-hover:text-[#8B9CFF] transition-colors">
                  {dest.name}
                </span>
              </a>
            ))}
          </motion.div>
        </div>

        {/* Features Section */}
        <section className="relative z-10 max-w-6xl mx-auto px-6 py-20">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="text-center mb-14"
          >
            <p className="text-[#8B9CFF] text-xs font-bold tracking-widest uppercase mb-3">How it works</p>
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white">
              AI agents that think like a travel expert
            </h2>
          </motion.div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {features.map((feature, i) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: i * 0.08 }}
                className="group bg-white dark:bg-[#151923] rounded-2xl p-6 border border-gray-200 dark:border-gray-800 hover:border-[#8B9CFF]/30 transition-all duration-300 hover:shadow-lg hover:shadow-indigo-500/5"
              >
                <div className="w-12 h-12 rounded-xl bg-indigo-50 dark:bg-indigo-900/20 flex items-center justify-center mb-4 text-2xl group-hover:scale-110 transition-transform duration-300">
                  {feature.icon}
                </div>
                <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">{feature.title}</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </section>

        {/* CTA Section */}
        <section className="relative z-10 max-w-4xl mx-auto px-6 py-20 text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="bg-gradient-to-br from-indigo-600 to-purple-700 dark:from-indigo-800 dark:to-purple-900 rounded-3xl p-10 sm:p-14 shadow-2xl shadow-indigo-500/20 relative overflow-hidden"
          >
            <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full blur-3xl"></div>
            <div className="absolute bottom-0 left-0 w-48 h-48 bg-purple-300/10 rounded-full blur-3xl"></div>
            <div className="relative z-10">
              <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
                Ready to plan your next trip?
              </h2>
              <p className="text-indigo-200 text-base sm:text-lg mb-8 max-w-xl mx-auto">
                Let TripMind&apos;s AI agents handle the research, scheduling, and budgeting.
                You just enjoy the journey.
              </p>
              <a
                href="/plan"
                className="inline-flex items-center gap-2 px-8 py-4 bg-white text-indigo-700 font-bold rounded-2xl text-lg hover:bg-indigo-50 transition-colors shadow-lg"
              >
                Start planning → 
              </a>
            </div>
          </motion.div>
        </section>

        {/* Footer */}
        <footer className="border-t border-gray-200 dark:border-gray-800 py-8 px-6">
          <div className="max-w-5xl mx-auto flex flex-col sm:flex-row justify-between items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
            <div className="flex items-center gap-2">
              <span className="text-[#8B9CFF] font-bold">TripMind AI</span>
              <span>•</span>
              <span>Multi-Agent Travel Planning</span>
            </div>
            <div className="flex items-center gap-1">
              Built with <span className="text-red-500">♥</span> using CrewAI + Groq + Gemini
            </div>
          </div>
        </footer>
      </main>
    </div>
  );
}