import React from 'react';
import { VersionBadge } from './VersionBadge';

export const Footer: React.FC = () => {
  // Get the base API URL without the /api/v1 suffix for direct FastAPI endpoints
  const envApiUrl = process.env.REACT_APP_API_URL || "http://localhost:8888";
  const API_BASE_URL = envApiUrl.replace(/\/api\/v1$/, ''); // Remove /api/v1 suffix if present
  return (
    <footer className="mt-16 py-8 border-t border-slate-600/30 theme-bg-card/50">
      <div className="container mx-auto px-6">
        <div className="flex flex-col md:flex-row justify-center items-center gap-6">
          <div className="flex items-center gap-4">
            <VersionBadge variant="minimal" position="inline" showBackendVersion={true} />
          </div>
          
          <div className="flex flex-wrap gap-4 text-xs theme-text-secondary">
            <a href={`${API_BASE_URL}/docs`} target="_blank" rel="noopener noreferrer" className="hover:text-blue-400 transition-colors">
              API Documentation
            </a>
            <span>•</span>
            <a href={`${API_BASE_URL}/health`} target="_blank" rel="noopener noreferrer" className="hover:text-green-400 transition-colors">
              Health Check
            </a>
            <span>•</span>
            <a href={`${API_BASE_URL}/version`} target="_blank" rel="noopener noreferrer" className="hover:text-purple-400 transition-colors">
              Version Info
            </a>
            <span>•</span>
            <a href="https://github.com/Panosero/data-contracts-studio" target="_blank" rel="noopener noreferrer" className="hover:text-slate-300 transition-colors">
              GitHub
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};
