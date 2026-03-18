# React Frontend Integration Guide

## Overview

This guide explains how to integrate the AI-Based HR Management System backend APIs with your React frontend application.

## API Configuration

### Base URL
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

### CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:3000` (default React dev server)
- `http://localhost:3001` (alternative port)
- `http://127.0.0.1:3000`

**Allowed Methods:** GET, POST, PUT, DELETE, OPTIONS
**Allowed Headers:** Content-Type, Authorization
**Credentials:** Supported (for cookies/auth)

## Standard Response Format

All API endpoints return responses in this format:

### Success Response
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    // Response data here
  }
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error message",
  "error": "Detailed error description"
}
```

## React Setup

### 1. Install Axios
```bash
npm install axios
```

### 2. Create API Service (`src/services/api.js`)

```javascript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized - redirect to login
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

### 3. Create API Methods (`src/services/authService.js`)

```javascript
import api from './api';

export const authService = {
  // Register new user
  register: async (userData) => {
    try {
      const response = await api.post('/auth/register', userData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Login user
  login: async (credentials) => {
    try {
      const response = await api.post('/auth/login', credentials);
      if (response.data.success) {
        // Store token
        localStorage.setItem('token', response.data.data.token);
        localStorage.setItem('user', JSON.stringify(response.data.data.user));
      }
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Logout user
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  // Get current user
  getCurrentUser: () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },

  // Verify token
  verifyToken: async () => {
    try {
      const response = await api.get('/auth/verify');
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },
};
```

### 4. Job Service (`src/services/jobService.js`)

```javascript
import api from './api';

export const jobService = {
  // Get all jobs
  getAllJobs: async (params = {}) => {
    try {
      const response = await api.get('/jobs', { params });
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Get single job
  getJob: async (jobId) => {
    try {
      const response = await api.get(`/jobs/${jobId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Create job
  createJob: async (jobData) => {
    try {
      const response = await api.post('/jobs', jobData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Update job
  updateJob: async (jobId, jobData) => {
    try {
      const response = await api.put(`/jobs/${jobId}`, jobData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Delete job
  deleteJob: async (jobId) => {
    try {
      const response = await api.delete(`/jobs/${jobId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Get active jobs
  getActiveJobs: async () => {
    try {
      const response = await api.get('/jobs/active');
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },
};
```

### 5. Candidate Service (`src/services/candidateService.js`)

```javascript
import api from './api';

export const candidateService = {
  // Get all candidates (ranked)
  getAllCandidates: async (params = {}) => {
    try {
      const response = await api.get('/candidates', { params });
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Get candidates for specific job
  getCandidatesByJob: async (jobId, limit = 10) => {
    try {
      const response = await api.get(`/candidates/job/${jobId}`, {
        params: { limit },
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Create candidate
  createCandidate: async (candidateData) => {
    try {
      const response = await api.post('/candidates', candidateData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Update candidate status
  updateCandidateStatus: async (candidateId, status) => {
    try {
      const response = await api.put(`/candidates/${candidateId}/status`, {
        status,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },
};
```

### 6. Resume Service (`src/services/resumeService.js`)

```javascript
import api from './api';

export const resumeService = {
  // Upload resume
  uploadResume: async (formData) => {
    try {
      const response = await api.post('/resumes/upload-resume', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Parse resume
  parseResume: async (file) => {
    try {
      const formData = new FormData();
      formData.append('resume', file);

      const response = await api.post('/resumes/parse', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Calculate match score
  calculateMatch: async (resumeText, jobRequirements) => {
    try {
      const response = await api.post('/resumes/match', {
        resume_text: resumeText,
        job_requirements: jobRequirements,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Get detailed match analysis
  getDetailedMatch: async (resumeText, jobRequirements) => {
    try {
      const response = await api.post('/resumes/detailed-match', {
        resume_text: resumeText,
        job_requirements: jobRequirements,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Extract skills
  extractSkills: async (resumeText) => {
    try {
      const response = await api.post('/resumes/extract-skills', {
        resume_text: resumeText,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },
};
```

## React Component Examples

### Login Component

```javascript
import React, { useState } from 'react';
import { authService } from '../services/authService';

function Login() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authService.login(formData);
      
      if (response.success) {
        // Show success message
        alert(response.message);
        // Redirect to dashboard
        window.location.href = '/dashboard';
      }
    } catch (error) {
      setError(error.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Login</h2>
      
      {error && <div className="error">{error}</div>}
      
      <input
        type="email"
        placeholder="Email"
        value={formData.email}
        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
        required
      />
      
      <input
        type="password"
        placeholder="Password"
        value={formData.password}
        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
        required
      />
      
      <button type="submit" disabled={loading}>
        {loading ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
}

export default Login;
```

### Job List Component

```javascript
import React, { useState, useEffect } from 'react';
import { jobService } from '../services/jobService';

function JobList() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const response = await jobService.getAllJobs();
      
      if (response.success) {
        setJobs(response.data.jobs);
      }
    } catch (error) {
      setError(error.message || 'Failed to fetch jobs');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div>
      <h2>Job Listings ({jobs.length})</h2>
      
      {jobs.map((job) => (
        <div key={job._id} className="job-card">
          <h3>{job.job_title}</h3>
          <p>{job.description}</p>
          <p><strong>Location:</strong> {job.location}</p>
          <p><strong>Experience:</strong> {job.experience}</p>
          <p><strong>Skills:</strong> {job.required_skills}</p>
          <span className={`status ${job.status}`}>{job.status}</span>
        </div>
      ))}
    </div>
  );
}

export default JobList;
```

### Resume Upload Component

```javascript
import React, { useState } from 'react';
import { resumeService } from '../services/resumeService';

function ResumeUpload({ jobId }) {
  const [formData, setFormData] = useState({
    candidate_name: '',
    email: '',
    job_id: jobId,
  });
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      // Validate file type
      const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
      if (!allowedTypes.includes(selectedFile.type)) {
        alert('Only PDF and DOCX files are allowed');
        return;
      }
      setFile(selectedFile);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      alert('Please select a resume file');
      return;
    }

    setUploading(true);
    setMessage('');

    try {
      const formDataToSend = new FormData();
      formDataToSend.append('candidate_name', formData.candidate_name);
      formDataToSend.append('email', formData.email);
      formDataToSend.append('job_id', formData.job_id);
      formDataToSend.append('resume', file);

      const response = await resumeService.uploadResume(formDataToSend);
      
      if (response.success) {
        setMessage(response.message);
        // Reset form
        setFormData({ candidate_name: '', email: '', job_id: jobId });
        setFile(null);
      }
    } catch (error) {
      setMessage(error.message || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Upload Resume</h3>
      
      {message && <div className="message">{message}</div>}
      
      <input
        type="text"
        placeholder="Full Name"
        value={formData.candidate_name}
        onChange={(e) => setFormData({ ...formData, candidate_name: e.target.value })}
        required
      />
      
      <input
        type="email"
        placeholder="Email"
        value={formData.email}
        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
        required
      />
      
      <input
        type="file"
        accept=".pdf,.docx"
        onChange={handleFileChange}
        required
      />
      
      <button type="submit" disabled={uploading}>
        {uploading ? 'Uploading...' : 'Upload Resume'}
      </button>
    </form>
  );
}

export default ResumeUpload;
```

### Ranked Candidates Component

```javascript
import React, { useState, useEffect } from 'react';
import { candidateService } from '../services/candidateService';

function RankedCandidates({ jobId }) {
  const [candidates, setcandidates] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCandidates();
  }, [jobId]);

  const fetchCandidates = async () => {
    try {
      const response = await candidateService.getCandidatesByJob(jobId);
      
      if (response.success) {
        setCandidates(response.data.candidates);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const updateStatus = async (candidateId, newStatus) => {
    try {
      const response = await candidateService.updateCandidateStatus(
        candidateId,
        newStatus
      );
      
      if (response.success) {
        // Refresh candidates
        fetchCandidates();
      }
    } catch (error) {
      alert(error.message);
    }
  };

  if (loading) return <div>Loading candidates...</div>;

  return (
    <div>
      <h2>Ranked Candidates</h2>
      
      {candidates.map((candidate, index) => (
        <div key={candidate.candidate_id} className="candidate-card">
          <div className="rank">#{index + 1}</div>
          <h3>{candidate.candidate_name}</h3>
          <p>{candidate.email}</p>
          <div className="match-score">
            Match Score: <strong>{candidate.match_score}%</strong>
          </div>
          <div className="skills">
            {candidate.skills.map((skill) => (
              <span key={skill} className="skill-tag">{skill}</span>
            ))}
          </div>
          <select
            value={candidate.status}
            onChange={(e) => updateStatus(candidate.candidate_id, e.target.value)}
          >
            <option value="pending">Pending</option>
            <option value="shortlisted">Shortlisted</option>
            <option value="interviewed">Interviewed</option>
            <option value="rejected">Rejected</option>
            <option value="hired">Hired</option>
          </select>
        </div>
      ))}
    </div>
  );
}

export default RankedCandidates;
```

## Error Handling Best Practices

```javascript
// Centralized error handler
export const handleApiError = (error) => {
  if (error.response) {
    // Server responded with error
    const { data, status } = error.response;
    
    switch (status) {
      case 400:
        return data.message || 'Invalid request';
      case 401:
        return 'Please login to continue';
      case 403:
        return 'Access denied';
      case 404:
        return 'Resource not found';
      case 500:
        return 'Server error. Please try again later';
      default:
        return data.message || 'An error occurred';
    }
  } else if (error.request) {
    // Request made but no response
    return 'Network error. Please check your connection';
  } else {
    // Something else happened
    return error.message || 'An unexpected error occurred';
  }
};
```

## Testing the Integration

Run the test script to verify all endpoints:

```bash
python test_react_integration.py
```

This will test:
- ✅ JSON response format
- ✅ CORS headers
- ✅ Success/error responses
- ✅ All API endpoints

## Summary

The backend is now fully configured for React frontend integration with:

1. ✅ **CORS enabled** for localhost:3000
2. ✅ **Standardized JSON responses** (success, message, data)
3. ✅ **Proper HTTP status codes**
4. ✅ **Error handling** with detailed messages
5. ✅ **Request/response logging** for debugging
6. ✅ **JWT authentication** support
7. ✅ **File upload** support with multipart/form-data

Start your Flask backend and React frontend, and they will communicate seamlessly!
