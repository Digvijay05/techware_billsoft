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
                    DEFAULT: '#312e81', // Indigo 900
                    foreground: '#FFFFFF',
                },
                secondary: {
                    DEFAULT: '#10B981', // Emerald
                    foreground: '#FFFFFF',
                },
                destructive: {
                    DEFAULT: '#EF4444',
                    foreground: '#f8fafc',
                },
                muted: {
                    DEFAULT: '#f1f5f9',
                    foreground: '#64748b',
                },
                background: '#ffffff',
                foreground: '#0f172a',
                border: '#e2e8f0',
            }
        },
    },
    plugins: [],
}
