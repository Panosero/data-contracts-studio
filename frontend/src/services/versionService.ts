import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create a separate axios instance for version endpoint (not under /api/v1)
const versionClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface BackendVersion {
  version: string;
  name: string;
  build_date: string;
  environment: string;
  api_version: string;
}

export const versionService = {
  async getBackendVersion(): Promise<BackendVersion> {
    try {
      const response = await versionClient.get<BackendVersion>('/version');
      return response.data;
    } catch (error) {
      console.warn('Could not fetch backend version:', error);
      // Return fallback version info
      return {
        version: '0.0.1',
        name: 'Data Contracts Studio',
        build_date: new Date().toISOString(),
        environment: 'unknown',
        api_version: 'v1'
      };
    }
  },

  async getHealthStatus(): Promise<{ status: string; service: string }> {
    try {
      const response = await versionClient.get('/health');
      return response.data;
    } catch (error) {
      console.warn('Could not fetch health status:', error);
      return {
        status: 'unknown',
        service: 'Data Contracts Studio'
      };
    }
  }
};
