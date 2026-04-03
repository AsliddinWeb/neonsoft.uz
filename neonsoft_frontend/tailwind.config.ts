import type { Config } from 'tailwindcss'

export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#00D4AA',
          50: '#E6FFF9',
          100: '#CCFFF3',
          200: '#99FFE7',
          300: '#66FFDB',
          400: '#33FFCF',
          500: '#00D4AA',
          600: '#00AA88',
          700: '#008066',
          800: '#005544',
          900: '#002B22',
        },
        secondary: '#0A0F1E',
        accent: '#FF6B35',
        surface: '#111827',
      },
      fontFamily: {
        display: ['Syne', 'sans-serif'],
        sans: ['DM Sans', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'fade-up': 'fadeUp 0.6s ease forwards',
        'fade-in': 'fadeIn 0.4s ease forwards',
        glow: 'glow 2s ease-in-out infinite alternate',
        'spin-slow': 'spin 3s linear infinite',
      },
      keyframes: {
        fadeUp: {
          '0%': { opacity: '0', transform: 'translateY(30px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        glow: {
          '0%': { boxShadow: '0 0 20px #00D4AA33' },
          '100%': { boxShadow: '0 0 40px #00D4AA66' },
        },
      },
    },
  },
  plugins: [],
} satisfies Config
