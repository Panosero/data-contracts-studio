import React from 'react';
import { VersionBadge } from './VersionBadge';

export const Footer: React.FC = () => {
  return (
    <footer className="mt-16 py-8 border-t border-slate-600/30 theme-bg-card/50">
      <div className="container mx-auto px-6">
        <div className="flex flex-col md:flex-row justify-center items-center gap-6">
          <div className="flex items-center gap-4">
            <VersionBadge variant="minimal" position="inline" showBackendVersion={true} />
            
            <div className="flex items-center gap-2 text-xs theme-text-secondary">
              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>Ready for production</span>
            </div>
          </div>
          
          <div className="flex flex-wrap gap-4 text-xs theme-text-secondary">
            <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer" className="hover:text-blue-400 transition-colors">
              API Documentation
            </a>
            <span>•</span>
            <a href="http://localhost:8000/health" target="_blank" rel="noopener noreferrer" className="hover:text-green-400 transition-colors">
              Health Check
            </a>
            <span>•</span>
            <a href="http://localhost:8000/version" target="_blank" rel="noopener noreferrer" className="hover:text-purple-400 transition-colors">
              Version Info
            </a>
            <span>•</span>
            <a href="https://github.com/panoero/data-contracts-studio" target="_blank" rel="noopener noreferrer" className="hover:text-slate-300 transition-colors">
              GitHub
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};
