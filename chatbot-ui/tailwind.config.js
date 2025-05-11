// Renamed to tailwind.config.js.bak to disable Tailwind CSS configuration
// Backup of original tailwind.config.js content:
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
  