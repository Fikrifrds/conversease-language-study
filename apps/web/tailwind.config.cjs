/** @type {import("tailwindcss").Config} */
module.exports = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
    "./apps/web/app/**/*.{ts,tsx}",
    "./apps/web/components/**/*.{ts,tsx}",
    "./apps/web/lib/**/*.{ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        ink: "#1c1917",
        leaf: "#f97316",
        mint: "#ffedd5",
        sun: "#facc15",
        coral: "#c2410c",
        paper: "#fffaf5",
        clay: "#9a3412"
      },
      boxShadow: {
        soft: "0 16px 50px rgba(124, 45, 18, 0.14)"
      }
    }
  },
  plugins: []
};
