/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        cyber: {
          bg: "#06090e",
          card: "#0d131d",
          cardHover: "#131c2a",
          border: "#1c2638",
          borderGlow: "#2563eb33",
          cyan: "#00f0ff",
          cyanDim: "#00f0ff22",
          emerald: "#10b981",
          emeraldDim: "#10b98122",
          amber: "#f59e0b",
          amberDim: "#f59e0b22",
          rose: "#f43f5e",
          roseDim: "#f43f5e22",
          purple: "#a855f7",
          purpleDim: "#a855f722",
          text: "#f1f5f9",
          muted: "#94a3b8",
          dim: "#475569"
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace']
      },
      boxShadow: {
        'cyber-cyan': '0 0 25px -5px rgba(0, 240, 255, 0.25)',
        'cyber-emerald': '0 0 25px -5px rgba(16, 185, 129, 0.3)',
        'cyber-rose': '0 0 25px -5px rgba(244, 63, 94, 0.3)',
        'cyber-purple': '0 0 25px -5px rgba(168, 85, 247, 0.3)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'scan-line': 'scan 2.5s ease-in-out infinite',
      },
      keyframes: {
        scan: {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(1000%)' },
        }
      }
    },
  },
  plugins: [],
}
