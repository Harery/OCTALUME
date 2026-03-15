/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0fdfa',
          100: '#ccfbf1',
          200: '#99f6e4',
          300: '#5eead4',
          400: '#2dd4bf',
          500: '#00D4AA',
          600: '#00b89c',
          700: '#009c87',
          800: '#00806f',
          900: '#006458',
        },
        secondary: {
          50: '#f5f5f7',
          100: '#e5e5ea',
          200: '#c7c7cc',
          300: '#a1a1a6',
          400: '#8e8e93',
          500: '#636366',
          600: '#48484a',
          700: '#3a3a3c',
          800: '#2c2c2e',
          900: '#1A1A2E',
        },
        accent: '#FF6B35',
      },
    },
  },
  plugins: [],
}
