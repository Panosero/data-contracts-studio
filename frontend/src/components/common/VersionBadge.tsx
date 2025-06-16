import React, { useState, useEffect } from 'react';
import { getVersionInfo } from '../../version';
import { versionService, BackendVersion } from '../../services/versionService';

interface VersionBadgeProps {
  variant?: 'full' | 'minimal' | 'icon' | 'detailed';
  position?: 'fixed' | 'inline';
  className?: string;
  showBackendVersion?: boolean;
}

export const VersionBadge: React.FC<VersionBadgeProps> = ({ 
  variant = 'minimal', 
  position = 'fixed',
  className = '',
  showBackendVersion = false
}) => {
  const [backendVersion, setBackendVersion] = useState<BackendVersion | null>(null);
  const [showDetails, setShowDetails] = useState(false);
  const { version, appName, environment } = getVersionInfo();
  
  useEffect(() => {
    if (showBackendVersion || variant === 'detailed') {
      versionService.getBackendVersion().then(setBackendVersion);
    }
  }, [showBackendVersion, variant]);
  
  const baseClasses = "px-3 py-1 rounded-full text-xs font-medium transition-all duration-200 hover:scale-105 select-none cursor-pointer";
  
  const variantClasses = {
    full: "bg-gradient-to-r from-blue-500/20 to-purple-500/20 text-blue-400 border border-blue-400/30 backdrop-blur-sm",
    minimal: "bg-slate-800/80 text-slate-300 border border-slate-600/50 backdrop-blur-sm hover:bg-slate-700/80",
    icon: "bg-slate-900/90 text-slate-200 border border-slate-500/50 backdrop-blur-sm hover:bg-slate-800/90",
    detailed: "bg-gradient-to-r from-slate-800/90 to-slate-700/90 text-slate-200 border border-slate-500/50 backdrop-blur-sm hover:from-slate-700/90 hover:to-slate-600/90"
  };
  
  const positionClasses = position === 'fixed' 
    ? "fixed bottom-4 left-4 z-40" 
    : "inline-block";

  const versionsMatch = backendVersion?.version === version;

  const renderContent = () => {
    switch (variant) {
      case 'full':
        return (
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full animate-pulse ${versionsMatch ? 'bg-green-400' : 'bg-yellow-400'}`}></div>
            <span className="font-semibold">{appName}</span>
            <span className="opacity-75">v{version}</span>
            {environment === 'development' && (
              <span className="text-xs bg-yellow-500/20 text-yellow-400 px-2 py-0.5 rounded">
                DEV
              </span>
            )}
          </div>
        );
      
      case 'minimal':
        return (
          <div className="flex items-center gap-1.5">
            <div className={`w-1.5 h-1.5 rounded-full ${versionsMatch ? 'bg-blue-400' : 'bg-yellow-400'}`}></div>
            <span>v{version}</span>
          </div>
        );
      
      case 'icon':
        return (
          <div className="flex items-center gap-1">
            <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            <span>{version}</span>
          </div>
        );

      case 'detailed':
        return (
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${versionsMatch ? 'bg-green-400' : 'bg-yellow-400'}`}></div>
            <div className="flex flex-col">
              <span className="font-medium">Frontend v{version}</span>
              {backendVersion && (
                <span className="text-xs opacity-75">Backend v{backendVersion.version}</span>
              )}
            </div>
          </div>
        );
      
      default:
        return `v${version}`;
    }
  };

  const getTooltipText = () => {
    let tooltip = `${appName} v${version} (${environment})`;
    if (backendVersion) {
      tooltip += `\nBackend: v${backendVersion.version} (${backendVersion.environment})`;
      tooltip += `\nAPI: ${backendVersion.api_version}`;
      if (!versionsMatch) {
        tooltip += '\n⚠️ Version mismatch detected';
      }
    }
    return tooltip;
  };

  return (
    <div className="relative">
      <div 
        className={`${baseClasses} ${variantClasses[variant]} ${positionClasses} ${className}`}
        title={getTooltipText()}
        onClick={() => variant === 'detailed' && setShowDetails(!showDetails)}
      >
        {renderContent()}
      </div>

      {/* Detailed popup for fixed positioned badges */}
      {showDetails && position === 'fixed' && (
        <div className="fixed bottom-16 left-4 z-50 bg-slate-800/95 backdrop-blur-sm border border-slate-600/50 rounded-lg p-4 text-xs text-slate-200 shadow-xl">
          <div className="space-y-2">
            <div className="font-semibold text-blue-400">{appName}</div>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div>
                <div className="text-slate-400">Frontend:</div>
                <div>v{version}</div>
              </div>
              {backendVersion && (
                <div>
                  <div className="text-slate-400">Backend:</div>
                  <div>v{backendVersion.version}</div>
                </div>
              )}
            </div>
            <div className="pt-2 border-t border-slate-600/50">
              <div className="text-slate-400">Environment: {environment}</div>
              {backendVersion && (
                <div className="text-slate-400">API Version: {backendVersion.api_version}</div>
              )}
            </div>
            {!versionsMatch && (
              <div className="text-yellow-400 text-xs">
                ⚠️ Frontend/Backend version mismatch
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
