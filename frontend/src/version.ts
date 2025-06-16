/**
 * Version information for Data Contracts Studio Frontend
 * 
 * This module provides version and build information for the frontend application.
 * The version is managed centrally through the release script.
 */

export const VERSION = '0.0.6';
export const APP_NAME = 'Data Contracts Studio';
export const BUILD_DATE = new Date().toISOString();

export interface VersionInfo {
  version: string;
  appName: string;
  buildDate: string;
  environment: string;
}

export const getVersionInfo = (): VersionInfo => ({
  version: VERSION,
  appName: APP_NAME,
  buildDate: BUILD_DATE,
  environment: process.env.NODE_ENV || 'development',
});
