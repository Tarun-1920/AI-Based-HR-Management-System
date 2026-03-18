import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { handleApiError } from '../utils/api';
import '../styles/Login.css';

const Login = ({ onLogin }) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    role: 'hr'
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    // Clear error when user starts typing
    if (error) setError('');
  };

  const validateForm = () => {
    if (!formData.email) {
      setError('Email is required');
      return false;
    }
    if (!formData.password) {
      setError('Password is required');
      return false;
    }
    if (!/\S+@\S+\.\S+/.test(formData.email)) {
      setError('Please enter a valid email address');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    setIsLoading(true);
    setError('');
    setSuccess('');

    try {
      // Mock authentication - no backend required
      // In production, this would call: await authAPI.login(...)
      
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock user data
      const mockUser = {
        id: 'user_' + Math.random().toString(36).substr(2, 9),
        email: formData.email,
        role: formData.role,
        name: formData.role === 'hr' ? 'HR Manager' : 'Candidate User'
      };
      
      // Store mock token and user data
      localStorage.setItem('authToken', 'mock_token_' + Date.now());
      localStorage.setItem('userRole', formData.role);
      localStorage.setItem('userName', mockUser.name);
      localStorage.setItem('userEmail', formData.email);
      localStorage.setItem('userId', mockUser.id);

      // Show success message
      setSuccess(`Welcome back! Logging in as ${formData.role}...`);
      
      // Call parent callback to update app state
      setTimeout(() => {
        onLogin(formData.role);
      }, 1500);

    } catch (err) {
      const errorMessage = handleApiError(err);
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoLogin = (role) => {
    const demoCredentials = {
      hr: { email: 'hr@company.com', password: 'password123' },
      candidate: { email: 'candidate@email.com', password: 'password123' }
    };
    
    setFormData({
      ...demoCredentials[role],
      role: role
    });
    setError('');
  };

  return (
    <div className="login-container">
      <div className="login-background">
        <div className="floating-shapes">
          <div className="shape shape-1"></div>
          <div className="shape shape-2"></div>
          <div className="shape shape-3"></div>
          <div className="shape shape-4"></div>
        </div>
      </div>
      
      <div className="login-card">
        <div className="login-header">
          <div className="logo">
            <i className="fas fa-brain"></i>
          </div>
          <h1>AI HR Management System</h1>
          <p>Welcome back! Please sign in to your account</p>
        </div>

        {success && (
          <div className="success-message">
            <i className="fas fa-check-circle"></i>
            <span>{success}</span>
          </div>
        )}

        {error && (
          <div className="error-message">
            <i className="fas fa-exclamation-circle"></i>
            <span>{error}</span>
          </div>
        )}

        {success && (
          <div className="success-message">
            <i className="fas fa-check-circle"></i>
            <span>{success}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="role">Login As</label>
            <div className="role-selector">
              <div 
                className={`role-option ${formData.role === 'hr' ? 'active' : ''}`}
                onClick={() => setFormData({...formData, role: 'hr'})}
              >
                <i className="fas fa-user-tie"></i>
                <span>HR Manager</span>
              </div>
              <div 
                className={`role-option ${formData.role === 'candidate' ? 'active' : ''}`}
                onClick={() => setFormData({...formData, role: 'candidate'})}
              >
                <i className="fas fa-user"></i>
                <span>Candidate</span>
              </div>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <div className="input-wrapper">
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="Enter your email address"
                required
                disabled={isLoading}
              />
              <i className="fas fa-envelope"></i>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <div className="input-wrapper">
              <input
                type={showPassword ? "text" : "password"}
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Enter your password"
                required
                disabled={isLoading}
              />
              <i className="fas fa-lock"></i>
              <button
                type="button"
                className="toggle-password"
                onClick={() => setShowPassword(!showPassword)}
                disabled={isLoading}
              >
                <i className={showPassword ? "fas fa-eye-slash" : "fas fa-eye"}></i>
              </button>
            </div>
          </div>

          <button type="submit" className="login-btn" disabled={isLoading}>
            {isLoading ? (
              <>
                <i className="fas fa-spinner fa-spin"></i>
                Signing In...
              </>
            ) : (
              <>
                <i className="fas fa-sign-in-alt"></i>
                Sign In
              </>
            )}
          </button>
        </form>

        <div className="divider">
          <span>or try demo accounts</span>
        </div>

        <div className="demo-section">
          <h4>Quick Demo Access</h4>
          <div className="demo-buttons">
            <button 
              type="button" 
              className="demo-btn hr-demo"
              onClick={() => handleDemoLogin('hr')}
              disabled={isLoading}
            >
              <i className="fas fa-user-tie"></i>
              <div>
                <strong>HR Demo</strong>
                <small>hr@company.com</small>
              </div>
            </button>
            <button 
              type="button" 
              className="demo-btn candidate-demo"
              onClick={() => handleDemoLogin('candidate')}
              disabled={isLoading}
            >
              <i className="fas fa-user"></i>
              <div>
                <strong>Candidate Demo</strong>
                <small>candidate@email.com</small>
              </div>
            </button>
          </div>
        </div>

        <div className="login-footer">
          <p>
            Don't have an account? 
            <button 
              className="link-btn" 
              onClick={() => navigate('/register')}
              disabled={isLoading}
            >
              Sign Up
            </button>
          </p>
          <p style={{ marginTop: '10px', fontSize: '12px' }}>Powered by AI Technology</p>
        </div>
      </div>
    </div>
  );
};

export default Login;
