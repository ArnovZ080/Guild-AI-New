import React, { createContext, useContext, useEffect, useState } from 'react';

const ThemeContext = createContext({ theme: 'system', resolvedTheme: 'light', setTheme: () => {} });

export function useTheme() {
    return useContext(ThemeContext);
}

export function ThemeProvider({ children }) {
    const [theme, setThemeState] = useState(() => {
        if (typeof window !== 'undefined') {
            return localStorage.getItem('guild-theme') || 'system';
        }
        return 'system';
    });

    const [resolvedTheme, setResolvedTheme] = useState('light');

    const setTheme = (newTheme) => {
        setThemeState(newTheme);
        localStorage.setItem('guild-theme', newTheme);
    };

    const toggleTheme = () => {
        if (resolvedTheme === 'dark') {
            setTheme('light');
        } else {
            setTheme('dark');
        }
    };

    useEffect(() => {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

        const updateTheme = () => {
            let resolved;
            if (theme === 'system') {
                resolved = mediaQuery.matches ? 'dark' : 'light';
            } else {
                resolved = theme;
            }
            setResolvedTheme(resolved);

            const root = document.documentElement;
            if (resolved === 'dark') {
                root.classList.add('dark');
            } else {
                root.classList.remove('dark');
            }
        };

        updateTheme();
        mediaQuery.addEventListener('change', updateTheme);
        return () => mediaQuery.removeEventListener('change', updateTheme);
    }, [theme]);

    return (
        <ThemeContext.Provider value={{ theme, resolvedTheme, setTheme, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    );
}
