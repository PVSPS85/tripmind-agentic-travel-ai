import '../styles/globals.css';
import type { AppProps } from 'next/app';
import { useState, createContext, useEffect } from 'react';

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
      {/* We removed the dynamic wrapper here because we are applying it directly to the HTML tag above */}
      <div className="min-h-screen bg-white dark:bg-[#0B0F17] transition-colors duration-300">
        <Component {...pageProps} />
      </div>
    </ThemeContext.Provider>
  );
}