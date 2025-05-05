/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./index.html",
      "./src/**/*.{js,jsx,ts,tsx}", // ✅ Ensures all your JSX files are scanned
    ],
    theme: {
      extend: {},
    },
    plugins: [],
  };
  