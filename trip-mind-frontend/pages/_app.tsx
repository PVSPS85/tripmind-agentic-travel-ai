import '../styles/globals.css';
import type { AppProps } from 'next/app';
import { useState, createContext, useEffect } from 'react';
import Head from 'next/head';

export const ThemeContext = createContext({ isDark: true, toggleTheme: () => {} });

export default function App({ Component, pageProps }: AppProps) {
  const [isDark, setIsDark] = useState(true);

  // 1. When the app loads, check the browser's memory for a saved theme
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
      setIsDark(false);
      document.documentElement.classList.remove('dark');
    } else {
      setIsDark(true);
      document.documentElement.classList.add('dark');
    }
  }, []);

  // 2. When you click the toggle, update the state, the HTML class, AND save it to memory
  const toggleTheme = () => {
    setIsDark((prev) => {
      const newIsDark = !prev;
      if (newIsDark) {
        document.documentElement.classList.add('dark');
        localStorage.setItem('theme', 'dark');
      } else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
      }
      return newIsDark;
    });
  };

  return (
    <ThemeContext.Provider value={{ isDark, toggleTheme }}>
      <Head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
        <meta name="description" content="TripMind AI — Plan thoughtful group trips, guided by AI agents." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🧠</text></svg>" />
      </Head>
      <div className="min-h-screen bg-white dark:bg-[#0B0F17] transition-colors duration-300">
        <Component {...pageProps} />
      </div>
    </ThemeContext.Provider>
  );
}