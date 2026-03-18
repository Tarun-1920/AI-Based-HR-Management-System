import axios from 'axios';

// API Base URL - Change this to your backend URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    // Don't add Authorization header for login and register endpoints
    const isAuthEndpoint = config.url?.includes('/auth/login') || config.url?.includes('/auth/register');
    
    if (!isAuthEndpoint) {
      const token = localStorage.getItem('authToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('authToken');
      localStorage.removeItem('userRole');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ============================================
// Authentication API
// ============================================
export const authAPI = {
  register: async (email, password, name, role) => {
    try {
      const response = await apiClient.post('/auth/register', {
        email,
        password,
        name,
        role,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Registration failed' };
    }
  },

  login: async (email, password, role) => {
    try {
      const response = await apiClient.post('/auth/login', {
        email,
        password,
        role,
      });
      
      // Store token and role in localStorage
      if (response.data.token) {
        localStorage.setItem('authToken', response.data.token);
        localStorage.setItem('userRole', role);
        localStorage.setItem('userName', response.data.name || email);
      }
      
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Login failed' };
    }
  },

  logout: () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userRole');
    localStorage.removeItem('userName');
  },

  getAuthToken: () => localStorage.getItem('authToken'),
  getUserRole: () => localStorage.getItem('userRole'),
  getUserName: () => localStorage.getItem('userName'),
  isAuthenticated: () => !!localStorage.getItem('authToken'),
};

// ============================================
// Jobs API
// ============================================
export const jobsAPI = {
  getAllJobs: async () => {
    try {
      const response = await apiClient.get('/jobs');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch jobs' };
    }
  },

  getJobById: async (jobId) => {
    try {
      const response = await apiClient.get(`/jobs/${jobId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch job' };
    }
  },

  createJob: async (jobData) => {
    try {
      const response = await apiClient.post('/jobs', jobData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to create job' };
    }
  },

  updateJob: async (jobId, jobData) => {
    try {
      const response = await apiClient.put(`/jobs/${jobId}`, jobData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to update job' };
    }
  },

  deleteJob: async (jobId) => {
    try {
      const response = await apiClient.delete(`/jobs/${jobId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to delete job' };
    }
  },
};

// ============================================
// Candidates API
// ============================================
export const candidatesAPI = {
  getAllCandidates: async (filters = {}) => {
    try {
      const response = await apiClient.get('/candidates', { params: filters });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch candidates' };
    }
  },

  getCandidateById: async (candidateId) => {
    try {
      const response = await apiClient.get(`/candidates/${candidateId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch candidate' };
    }
  },

  uploadResume: async (formData, onUploadProgress) => {
    try {
      const response = await apiClient.post('/resumes/upload-resume', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          if (onUploadProgress) {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            onUploadProgress(percentCompleted);
          }
        },
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to upload resume' };
    }
  },

  updateCandidateStatus: async (candidateId, status) => {
    try {
      const response = await apiClient.patch(`/candidates/${candidateId}/status`, {
        status,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to update candidate status' };
    }
  },

  getCandidatesByJob: async (jobId) => {
    try {
      const response = await apiClient.get(`/candidates/job/${jobId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch candidates for job' };
    }
  },

  downloadResume: async (candidateId) => {
    try {
      const response = await apiClient.get(`/candidates/${candidateId}/resume`, {
        responseType: 'blob',
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to download resume' };
    }
  },
};

// ============================================
// AI API
// ============================================
export const aiAPI = {
  analyzeResume: async (resumeData) => {
    try {
      const response = await apiClient.post('/ai/analyze-resume', resumeData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to analyze resume' };
    }
  },

  matchCandidates: async (jobId) => {
    try {
      const response = await apiClient.post(`/ai/match-candidates/${jobId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to match candidates' };
    }
  },

  getMatchScore: async (candidateId, jobId) => {
    try {
      const response = await apiClient.get(
        `/ai/match-score/${candidateId}/${jobId}`
      );
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to get match score' };
    }
  },
};

// ============================================
// Dashboard API
// ============================================
export const dashboardAPI = {
  getStats: async () => {
    try {
      const response = await apiClient.get('/dashboard/stats');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch stats' };
    }
  },

  getRecentActivities: async () => {
    try {
      const response = await apiClient.get('/dashboard/activities');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch activities' };
    }
  },

  getTopCandidates: async () => {
    try {
      const response = await apiClient.get('/dashboard/top-candidates');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch top candidates' };
    }
  },
};

// ============================================
// Error Handler Utility
// ============================================
export const handleApiError = (error) => {
  console.log('API Error:', error); // Debug log
  if (error.response) {
    // Server responded with error status
    return error.response.data?.error || error.response.data?.message || 'An error occurred';
  } else if (error.request) {
    // Request made but no response
    return 'No response from server. Please check your connection.';
  } else {
    // Error in request setup
    return error.message || 'An error occurred';
  }
};

// ============================================
// Success Handler Utility
// ============================================
export const handleApiSuccess = (response) => {
  return response?.message || 'Operation successful';
};

export default apiClient;
