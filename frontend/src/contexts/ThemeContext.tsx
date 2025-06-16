import React, { createContext, useContext, useState, useEffect } from "react";

export type Theme = "dark"; // Only dark mode for now

interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
};

interface ThemeProviderProps {
  children: React.ReactNode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [theme, setTheme] = useState<Theme>("dark"); // Always dark mode

  useEffect(() => {
    // Always apply dark theme
    document.documentElement.className = "dark";
  }, []);

  const toggleTheme = () => {
    // Show coming soon notice instead of switching themes
    alert(
      "🎨 More themes coming soon!\n\nWe're working on Light Mode and Salmon Mode.\nStay tuned for updates!",
    );
  };

  return (
    <ThemeContext.Provider value={{ theme, setTheme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};
