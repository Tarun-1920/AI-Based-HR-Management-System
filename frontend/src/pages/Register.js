import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI, handleApiError } from '../utils/api';
import '../styles/Register.css';

const Register = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'Candidate'
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    if (error) setError('');
  };

  const validateForm = () => {
    if (!formData.name.trim()) {
      setError('Name is required');
      return false;
    }
    if (!formData.email) {
      setError('Email is required');
      return false;
    }
    if (!/\S+@\S+\.\S+/.test(formData.email)) {
      setError('Please enter a valid email address');
      return false;
    }
    if (!formData.password) {
      setError('Password is required');
      return false;
    }
    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters');
      return false;
    }
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
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
      console.log('Attempting registration with:', {
        email: formData.email,
        name: formData.name,
        role: formData.role
      });
      
      const response = await authAPI.register(
        formData.email,
        formData.password,
        formData.name,
        formData.role
      );
      
      console.log('Registration successful:', response);
      
      setSuccess('Registration successful! Redirecting to login...');
      
      setTimeout(() => {
        navigate('/login');
      }, 2000);

    } catch (err) {
      console.error('Registration error:', err);
      const errorMessage = handleApiError(err);
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="register-container">
      <div className="register-background">
        <div className="floating-shapes">
          <div className="shape shape-1"></div>
          <div className="shape shape-2"></div>
          <div className="shape shape-3"></div>
          <div className="shape shape-4"></div>
        </div>
      </div>
      
      <div className="register-card">
        <div className="register-header">
          <div className="logo">
            <i className="fas fa-brain"></i>
          </div>
          <h1>Create Your Account</h1>
          <p>Join our AI-powered HR Management System</p>
        </div>

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

        <form onSubmit={handleSubmit} className="register-form">
          <div className="form-group">
            <label htmlFor="role">I am registering as</label>
            <div className="role-selector">
              <div 
                className={`role-option ${formData.role === 'Candidate' ? 'active' : ''}`}
                onClick={() => setFormData({...formData, role: 'Candidate'})}
              >
                <i className="fas fa-user"></i>
                <div>
                  <strong>Candidate</strong>
                  <small>Looking for job opportunities</small>
                </div>
              </div>
              <div 
                className={`role-option ${formData.role === 'HR' ? 'active' : ''}`}
                onClick={() => setFormData({...formData, role: 'HR'})}
              >
                <i className="fas fa-user-tie"></i>
                <div>
                  <strong>HR Manager</strong>
                  <small>Recruiting and managing candidates</small>
                </div>
              </div>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="name">Full Name</label>
            <div className="input-wrapper">
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Enter your full name"
                required
                disabled={isLoading}
              />
              <i className="fas fa-user"></i>
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
                placeholder="Create a password (min 6 characters)"
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

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <div className="input-wrapper">
              <input
                type={showConfirmPassword ? "text" : "password"}
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                placeholder="Re-enter your password"
                required
                disabled={isLoading}
              />
              <i className="fas fa-lock"></i>
              <button
                type="button"
                className="toggle-password"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                disabled={isLoading}
              >
                <i className={showConfirmPassword ? "fas fa-eye-slash" : "fas fa-eye"}></i>
              </button>
            </div>
          </div>

          <button type="submit" className="register-btn" disabled={isLoading}>
            {isLoading ? (
              <>
                <i className="fas fa-spinner fa-spin"></i>
                Creating Account...
              </>
            ) : (
              <>
                <i className="fas fa-user-plus"></i>
                Create Account
              </>
            )}
          </button>
        </form>

        <div className="register-footer">
          <p>
            Already have an account? 
            <button 
              className="link-btn" 
              onClick={() => navigate('/login')}
              disabled={isLoading}
            >
              Sign In
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
