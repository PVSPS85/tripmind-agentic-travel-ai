/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class', 
  theme: {
    extend: {
      colors: {
        background: 'var(--background)',
        surface: 'var(--surface)',
        surface2: 'var(--surface-2)',
        foreground: 'var(--foreground)',
        muted: 'var(--text-muted)',
        subtle: 'var(--text-subtle)',
        primary: {
          DEFAULT: 'var(--primary)',
          soft: 'var(--primary-soft)',
        },
        accent: 'var(--accent)',
        border: 'var(--border)',
        success: 'var(--success)',
        destructive: 'var(--destructive)',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Plus Jakarta Sans', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      borderRadius: {
        'card': '16px',
        'btn': '12px',
        'tag': '999px',
      },
      boxShadow: {
        'soft': '0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04)',
      }
    },
  },
  plugins: [],
}