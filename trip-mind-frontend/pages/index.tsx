import React, { useContext } from 'react';
import Head from 'next/head';
import { ThemeContext } from './_app';

export default function Home() {
  const { isDark, toggleTheme } = useContext(ThemeContext);
  return (
    <div className="min-h-screen text-gray-900 dark:text-gray-100 font-sans flex flex-col">
      <Head><title>TripMind AI</title></Head>
      <nav className="border-b border-gray-200 dark:border-gray-800 p-6 flex justify-between items-center">
        <span className="text-xl font-bold text-[#8B9CFF]">TripMind AI</span>
        <button onClick={toggleTheme} className="p-2 border rounded">{isDark ? '☼' : '☾'}</button>
      </nav>
      <main className="flex-grow flex flex-col items-center justify-center p-6 text-center">
        <h1 className="text-6xl font-bold mb-6">Plan thoughtful group trips, <br/> <span className="text-[#8B9CFF]">guided by AI.</span></h1>
        <div className="flex gap-4 relative z-50">
          <a href="/plan" className="px-8 py-4 bg-[#8B9CFF] text-black font-bold rounded-xl">Plan my trip →</a>
          <a href="/dashboard/123" className="px-8 py-4 bg-gray-800 text-white rounded-xl">See demo trip</a>
        </div>
      </main>
    </div>
  );
}