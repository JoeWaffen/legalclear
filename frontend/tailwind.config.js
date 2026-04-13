/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: "#1e3a5f",
        teal: "#0d9488",
        surface: "#f8fafc",
        text_dark: "#1e293b",
        red_flag: "#dc2626",
        yellow_flag: "#d97706",
        green_flag: "#16a34a",
        border_color: "#e2e8f0"
      }
    },
  },
  plugins: [],
}
