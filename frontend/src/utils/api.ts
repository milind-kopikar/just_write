import axios from 'axios';

// In production (Railway), NEXT_PUBLIC_API_URL is set to the backend service URL.
// In local development, fall back to localhost detection for Windows compatibility.
const getBaseUrl = () => {
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname;
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
