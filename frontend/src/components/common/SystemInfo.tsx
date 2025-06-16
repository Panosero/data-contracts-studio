import React, { useEffect, useState } from 'react';
import { getVersionInfo } from '../../version';
import { versionService, BackendVersion } from '../../services/versionService';

export const SystemInfo: React.FC = () => {
  const [backendVersion, setBackendVersion] = useState<BackendVersion | null>(null);
  const [healthStatus, setHealthStatus] = useState<{ status: string; service: string } | null>(null);
  const [loading, setLoading] = useState(true);
  
  const frontendInfo = getVersionInfo();

  useEffect(() => {
    const fetchSystemInfo = async () => {
      try {
        const [backend, health] = await Promise.all([
          versionService.getBackendVersion(),
          versionService.getHealthStatus()
        ]);
        setBackendVersion(backend);
        setHealthStatus(health);
      } catch (error) {
        console.error('Failed to fetch system info:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchSystemInfo();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'healthy':
        return 'text-green-400';
      case 'unhealthy':
        return 'text-red-400';
      default:
        return 'text-yellow-400';
    }
  };

  const versionsMatch = backendVersion?.version === frontendInfo.version;

  if (loading) {
    return (
      <div className="p-6 theme-bg-card rounded-xl border border-slate-600/30">
        <div className="animate-pulse">
          <div className="h-4 bg-slate-700 rounded w-1/4 mb-4"></div>
          <div className="space-y-2">
            <div className="h-3 bg-slate-700 rounded w-3/4"></div>
            <div className="h-3 bg-slate-700 rounded w-1/2"></div>
            <div className="h-3 bg-slate-700 rounded w-2/3"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 theme-bg-card rounded-xl border border-slate-600/30 theme-shadow-lg">
      <h3 className="text-lg font-semibold theme-text-primary mb-4 flex items-center gap-2">
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        System Information
      </h3>
      
      <div className="space-y-4">
        {/* Version Compatibility */}
        <div className="flex items-center justify-between p-3 rounded-lg bg-slate-800/50">
          <span className="text-sm font-medium">Version Status</span>
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${versionsMatch ? 'bg-green-400' : 'bg-yellow-400'}`}></div>
            <span className={`text-sm ${versionsMatch ? 'text-green-400' : 'text-yellow-400'}`}>
              {versionsMatch ? 'Synchronized' : 'Version Mismatch'}
            </span>
          </div>
        </div>

        {/* Frontend Info */}
        <div className="grid grid-cols-2 gap-4">
          <div className="p-3 rounded-lg bg-blue-500/10 border border-blue-500/20">
            <div className="text-sm font-medium text-blue-400 mb-2">Frontend</div>
            <div className="space-y-1 text-xs theme-text-secondary">
              <div>Version: <span className="font-mono text-blue-300">v{frontendInfo.version}</span></div>
              <div>Environment: <span className="font-mono">{frontendInfo.environment}</span></div>
              <div>Build: <span className="font-mono">{new Date(frontendInfo.buildDate).toLocaleDateString()}</span></div>
            </div>
          </div>

          {/* Backend Info */}
          <div className="p-3 rounded-lg bg-green-500/10 border border-green-500/20">
            <div className="text-sm font-medium text-green-400 mb-2">Backend</div>
            <div className="space-y-1 text-xs theme-text-secondary">
              {backendVersion ? (
                <>
                  <div>Version: <span className="font-mono text-green-300">v{backendVersion.version}</span></div>
                  <div>Environment: <span className="font-mono">{backendVersion.environment}</span></div>
                  <div>API: <span className="font-mono">{backendVersion.api_version}</span></div>
                </>
              ) : (
                <div className="text-red-400">Connection failed</div>
              )}
            </div>
          </div>
        </div>

        {/* Health Status */}
        {healthStatus && (
          <div className="flex items-center justify-between p-3 rounded-lg bg-slate-800/50">
            <span className="text-sm font-medium">Backend Health</span>
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${healthStatus.status === 'healthy' ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`}></div>
              <span className={`text-sm font-mono ${getStatusColor(healthStatus.status)}`}>
                {healthStatus.status.toUpperCase()}
              </span>
            </div>
          </div>
        )}

        {/* Version Mismatch Warning */}
        {!versionsMatch && backendVersion && (
          <div className="p-3 rounded-lg bg-yellow-500/10 border border-yellow-500/20">
            <div className="flex items-center gap-2 text-yellow-400 text-sm">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
              <span className="font-medium">Version Mismatch Detected</span>
            </div>
            <p className="text-xs theme-text-secondary mt-1">
              Frontend and backend versions don't match. This may cause compatibility issues.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
