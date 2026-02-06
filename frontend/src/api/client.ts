import axios from 'axios'

// Use environment variable for API URL, fallback to localhost for development
// For production, set VITE_API_URL to your backend URL (e.g., Railway, Render, etc.)
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export default apiClient
