import axios from 'axios';

// On Windows, localhost vs 127.0.0.1 can cause CORS issues.
// This helper ensures we use the same hostname as the browser if possible, 
// defaulting to 127.0.0.1 which is more stable for the backend.
const getBaseUrl = () => {
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname;
    // If we are on localhost, use localhost for API too to avoid cross-origin logic
    if (hostname === 'localhost') return 'http://localhost:8000';
  }
  return 'http://127.0.0.1:8000';
};

export const API_BASE_URL = getBaseUrl();

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
});

export default api;
