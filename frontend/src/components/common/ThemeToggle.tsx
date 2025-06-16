import React from 'react';
import { useTheme } from '../../contexts/ThemeContext';

export const ThemeToggle: React.FC = () => {
  const { toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      className="group flex items-center justify-center w-12 h-12 rounded-full backdrop-blur-xl bg-gray-800/80 border border-gray-600/50 text-gray-100 hover:bg-gray-700/90 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500/50 shadow-lg hover:shadow-xl hover:scale-110"
      title="More themes coming soon! 🎨"
    >
      <span className="text-lg group-hover:scale-110 transition-transform duration-200">🌙</span>
    </button>
  );
};
