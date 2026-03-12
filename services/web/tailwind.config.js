/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: ["class"],
    content: [
        './pages/**/*.{js,jsx}',
        './components/**/*.{js,jsx}',
        './app/**/*.{js,jsx}',
        './src/**/*.{js,jsx}',
    ],
    prefix: "",
    theme: {
        container: {
            center: true,
            padding: "2rem",
            screens: {
                "2xl": "1400px",
            },
        },
        extend: {
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
                heading: ['"Space Grotesk"', 'sans-serif'],
            },
            colors: {
                // Primary Accent — Cobalt Blue
                cobalt: {
                    DEFAULT: '#1a6fff',
                    light: '#4d8fff',
                    dark: '#0f4fcc',
                    glow: 'rgba(26, 111, 255, 0.15)',
                },

                // Dark Surfaces
                surface: {
                    base: '#03050a',
                    raised: '#070b14',
                    card: '#0d1628',
                    overlay: '#111b2e',
                    border: 'rgba(255, 255, 255, 0.08)',
                },

                // Functional Colors (muted for dark mode)
                status: {
                    success: '#22c55e',
                    warning: '#f59e0b',
                    critical: '#ef4444',
                },

                // Shadcn/UI semantic tokens
                border: "hsl(var(--border))",
                input: "hsl(var(--input))",
                ring: "hsl(var(--ring))",
                background: "hsl(var(--background))",
                foreground: "hsl(var(--foreground))",
                primary: {
                    DEFAULT: "hsl(var(--primary))",
                    foreground: "hsl(var(--primary-foreground))",
                },
                secondary: {
                    DEFAULT: "hsl(var(--secondary))",
                    foreground: "hsl(var(--secondary-foreground))",
                },
                destructive: {
                    DEFAULT: "hsl(var(--destructive))",
                    foreground: "hsl(var(--destructive-foreground))",
                },
                muted: {
                    DEFAULT: "hsl(var(--muted))",
                    foreground: "hsl(var(--muted-foreground))",
                },
                accent: {
                    DEFAULT: "hsl(var(--accent))",
                    foreground: "hsl(var(--accent-foreground))",
                },
                popover: {
                    DEFAULT: "hsl(var(--popover))",
                    foreground: "hsl(var(--popover-foreground))",
                },
                card: {
                    DEFAULT: "hsl(var(--card))",
                    foreground: "hsl(var(--card-foreground))",
                },
            },
            borderRadius: {
                lg: "var(--radius)",
                md: "calc(var(--radius) - 2px)",
                sm: "calc(var(--radius) - 4px)",
            },
            keyframes: {
                "accordion-down": {
                    from: { height: "0" },
                    to: { height: "var(--radix-accordion-content-height)" },
                },
                "accordion-up": {
                    from: { height: "var(--radix-accordion-content-height)" },
                    to: { height: "0" },
                },
                'shimmer': {
                    '100%': { transform: 'translateX(100%)' },
                },
                'glow': {
                    '0%, 100%': { opacity: 0.7 },
                    '50%': { opacity: 1 },
                },
                'pulse-slow': {
                    '0%, 100%': { opacity: 0.03, transform: 'scale(1)' },
                    '50%': { opacity: 0.06, transform: 'scale(1.05)' },
                },
            },
            animation: {
                "accordion-down": "accordion-down 0.2s ease-out",
                "accordion-up": "accordion-up 0.2s ease-out",
                'pulse-gentle': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'shimmer': 'shimmer 2s infinite',
                'glow': 'glow 2s ease-in-out infinite alternate',
                'pulse-slow': 'pulse-slow 15s ease-in-out infinite alternate',
            },
        },
    },
    plugins: [require("tailwindcss-animate")],
}
