/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#1a365d",
        secondary: "#2d3748",
        accent: "#ed8936",
      },
      scale: {
        '98': '0.98',
        '102': '1.02',
      }
    },
  },
  plugins: [],
} 