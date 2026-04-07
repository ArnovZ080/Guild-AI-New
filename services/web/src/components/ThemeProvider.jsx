import React, { createContext, useContext, useEffect } from 'react';

const ThemeContext = createContext({ theme: 'dark', resolvedTheme: 'dark', setTheme: () => {} });

export function useTheme() {
    return useContext(ThemeContext);
}

/**
 * ThemeProvider — hardcoded to dark mode.
 * Light mode removed pre-launch to avoid text-invisible bugs.
 */
export function ThemeProvider({ children }) {
    useEffect(() => {
        document.documentElement.classList.add('dark');
    }, []);

    return (
        <ThemeContext.Provider value={{ theme: 'dark', resolvedTheme: 'dark', setTheme: () => {} }}>
            {children}
        </ThemeContext.Provider>
    );
}
