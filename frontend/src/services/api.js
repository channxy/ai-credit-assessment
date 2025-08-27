import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Credit Assessment API
export const creditAPI = {
  // Get credit assessment
  assessCredit: (userId, options = {}) =>
    api.post('/api/v1/credit/assess', { user_id: userId, ...options }),

  // Get user assessments
  getUserAssessments: (userId) =>
    api.get(`/api/v1/credit/assessments/${userId}`),

  // Create transaction
  createTransaction: (transaction) =>
    api.post('/api/v1/credit/transactions', transaction),

  // Get user transactions
  getUserTransactions: (userId) =>
    api.get(`/api/v1/credit/transactions/${userId}`),

  // Create/update user profile
  createUserProfile: (profile) =>
    api.post('/api/v1/credit/profiles', profile),

  // Get user profile
  getUserProfile: (userId) =>
    api.get(`/api/v1/credit/profiles/${userId}`),
};

// Simulation API
export const simulationAPI = {
  // Run scenario simulation
  runSimulation: (simulation) =>
    api.post('/api/v1/simulation/scenario', simulation),

  // Get simulation history
  getSimulationHistory: (userId) =>
    api.get(`/api/v1/simulation/history/${userId}`),
};

// Recommendations API
export const recommendationsAPI = {
  // Get recommendations
  getRecommendations: (userId) =>
    api.get(`/api/v1/recommendations/${userId}`),

  // Get improvement plan
  getImprovementPlan: (userId) =>
    api.get(`/api/v1/recommendations/${userId}/improvement-plan`),
};

// Users API
export const usersAPI = {
  // Get all users
  getUsers: () => api.get('/api/v1/users'),

  // Get specific user
  getUser: (userId) => api.get(`/api/v1/users/${userId}`),
};

// Health check
export const healthAPI = {
  checkHealth: () => api.get('/health'),
};

export { api };
