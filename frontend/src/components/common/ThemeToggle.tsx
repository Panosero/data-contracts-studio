import React from 'react';
import { useTheme } from '../../contexts/ThemeContext';

export const ThemeToggle: React.FC = () => {
  const { theme, toggleTheme } = useTheme();

  const getThemeIcon = () => {
    switch (theme) {
      case 'light':
        return '☀️';
      case 'dark':
        return '🌙';
      case 'salmon':
        return '🐠';
      default:
        return '☀️';
    }
  };

  const getThemeLabel = () => {
    switch (theme) {
      case 'light':
        return 'Light';
      case 'dark':
        return 'Dark';
      case 'salmon':
        return 'Salmon';
      default:
        return 'Light';
    }
  };

  return (
    <button
      onClick={toggleTheme}
      className="group flex items-center justify-center w-12 h-12 rounded-full backdrop-blur-xl bg-white/80 dark:bg-gray-800/80 salmon:bg-orange-100/80 border border-white/50 dark:border-gray-600/50 salmon:border-orange-200/50 theme-text-primary hover:bg-white/90 dark:hover:bg-gray-700/90 salmon:hover:bg-orange-100/90 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500/50 theme-shadow-lg hover:theme-shadow-xl hover:scale-110"
      title={`Switch to ${theme === 'light' ? 'dark' : theme === 'dark' ? 'salmon' : 'light'} mode`}
    >
      <span className="text-lg group-hover:scale-110 transition-transform duration-200">{getThemeIcon()}</span>
    </button>
  );
};
