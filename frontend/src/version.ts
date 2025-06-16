// Version information for Data Contracts Studio Frontend
export const VERSION = '0.0.1';
export const APP_NAME = 'Data Contracts Studio';
export const BUILD_DATE = new Date().toISOString();

export const getVersionInfo = () => ({
  version: VERSION,
  appName: APP_NAME,
  buildDate: BUILD_DATE,
  environment: process.env.NODE_ENV || 'development',
});
