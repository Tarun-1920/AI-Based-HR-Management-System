import React, { useState } from 'react';
import { jobsAPI, handleApiError } from '../utils/api';
import '../styles/PostJob.css';

const PostJob = () => {
  const [jobData, setJobData] = useState({
    title: '',
    description: '',
    skills: '',
    experience: '',
    location: '',
    jobType: 'full-time',
    salary: '',
    department: ''
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [showSuccess, setShowSuccess] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const validateForm = () => {
    const newErrors = {};

    if (!jobData.title.trim()) {
      newErrors.title = 'Job title is required';
    }
    if (!jobData.description.trim()) {
      newErrors.description = 'Job description is required';
    }
    if (jobData.description.trim().length < 50) {
      newErrors.description = 'Job description must be at least 50 characters';
    }
    if (!jobData.skills.trim()) {
      newErrors.skills = 'Required skills are required';
    }
    if (!jobData.experience.trim()) {
      newErrors.experience = 'Experience requirement is required';
    }
    if (!jobData.location.trim()) {
      newErrors.location = 'Location is required';
    }

    return newErrors;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setJobData(prev => ({
      ...prev,
      [name]: value
    }));
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const newErrors = validateForm();
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setIsSubmitting(true);
    setErrors({});
    setErrorMessage('');

    try {
      // Prepare data for API
      const postData = {
        title: jobData.title,
        description: jobData.description,
        required_skills: jobData.skills.split(',').map(skill => skill.trim()),
        experience_required: jobData.experience,
        location: jobData.location,
        job_type: jobData.jobType,
        salary: jobData.salary || null,
        department: jobData.department || null,
        posted_date: new Date().toISOString()
      };

      // Call API to create job
      const response = await jobsAPI.createJob(postData);

      // Show success message
      setSuccessMessage(
        `Job "${jobData.title}" posted successfully! Job ID: ${response.jobId || 'JOB-' + Math.floor(Math.random() * 10000)}`
      );
      setShowSuccess(true);

      // Reset form
      setJobData({
        title: '',
        description: '',
        skills: '',
        experience: '',
        location: '',
        jobType: 'full-time',
        salary: '',
        department: ''
      });

      // Hide success message after 5 seconds
      setTimeout(() => {
        setShowSuccess(false);
      }, 5000);

    } catch (error) {
      const errorMsg = handleApiError(error);
      setErrorMessage(errorMsg);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleReset = () => {
    setJobData({
      title: '',
      description: '',
      skills: '',
      experience: '',
      location: '',
      jobType: 'full-time',
      salary: '',
      department: ''
    });
    setErrors({});
    setShowSuccess(false);
    setErrorMessage('');
  };

  return (
    <div className="post-job-container">
      <div className="page-header">
        <div className="header-content">
          <h1>
            <i className="fas fa-plus-circle"></i>
            Post a New Job
          </h1>
          <p>Create a new job opening and let AI find the best candidates for you</p>
        </div>
        <div className="header-icon">
          <i className="fas fa-briefcase"></i>
        </div>
      </div>

      {showSuccess && (
        <div className="success-message">
          <div className="success-content">
            <i className="fas fa-check-circle"></i>
            <div>
              <h3>Job Posted Successfully!</h3>
              <p>{successMessage}</p>
            </div>
          </div>
          <button 
            className="close-success"
            onClick={() => setShowSuccess(false)}
          >
            <i className="fas fa-times"></i>
          </button>
        </div>
      )}

      {errorMessage && (
        <div className="error-message">
          <i className="fas fa-exclamation-circle"></i>
          <span>{errorMessage}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="job-form">
        <div className="form-section">
          <div className="section-header">
            <h2>
              <i className="fas fa-info-circle"></i>
              Basic Information
            </h2>
            <p>Enter the basic details about the job position</p>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="title">
                Job Title
                <span className="required">*</span>
              </label>
              <input
                type="text"
                id="title"
                name="title"
                value={jobData.title}
                onChange={handleChange}
                placeholder="e.g. Senior Python Developer"
                className={errors.title ? 'error' : ''}
                disabled={isSubmitting}
              />
              {errors.title && (
                <span className="error-text">
                  <i className="fas fa-exclamation-triangle"></i>
                  {errors.title}
                </span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="department">
                Department
              </label>
              <input
                type="text"
                id="department"
                name="department"
                value={jobData.department}
                onChange={handleChange}
                placeholder="e.g. Engineering, Sales"
                disabled={isSubmitting}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="location">
                Location
                <span className="required">*</span>
              </label>
              <input
                type="text"
                id="location"
                name="location"
                value={jobData.location}
                onChange={handleChange}
                placeholder="e.g. New York, NY / Remote"
                className={errors.location ? 'error' : ''}
                disabled={isSubmitting}
              />
              {errors.location && (
                <span className="error-text">
                  <i className="fas fa-exclamation-triangle"></i>
                  {errors.location}
                </span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="jobType">
                Job Type
              </label>
              <select
                id="jobType"
                name="jobType"
                value={jobData.jobType}
                onChange={handleChange}
                disabled={isSubmitting}
              >
                <option value="full-time">Full Time</option>
                <option value="part-time">Part Time</option>
                <option value="contract">Contract</option>
                <option value="internship">Internship</option>
                <option value="temporary">Temporary</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="experience">
                Experience Required
                <span className="required">*</span>
              </label>
              <input
                type="text"
                id="experience"
                name="experience"
                value={jobData.experience}
                onChange={handleChange}
                placeholder="e.g. 2-4 years"
                className={errors.experience ? 'error' : ''}
                disabled={isSubmitting}
              />
              {errors.experience && (
                <span className="error-text">
                  <i className="fas fa-exclamation-triangle"></i>
                  {errors.experience}
                </span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="salary">
                Salary Range (Optional)
              </label>
              <input
                type="text"
                id="salary"
                name="salary"
                value={jobData.salary}
                onChange={handleChange}
                placeholder="e.g. $80,000 - $120,000"
                disabled={isSubmitting}
              />
            </div>
          </div>
        </div>

        <div className="form-section">
          <div className="section-header">
            <h2>
              <i className="fas fa-file-alt"></i>
              Job Details
            </h2>
            <p>Provide detailed information about the position</p>
          </div>

          <div className="form-group full-width">
            <label htmlFor="description">
              Job Description
              <span className="required">*</span>
            </label>
            <textarea
              id="description"
              name="description"
              value={jobData.description}
              onChange={handleChange}
              rows="6"
              placeholder="Describe the role, responsibilities, and what the candidate will be doing. Include key responsibilities, day-to-day tasks, and career growth opportunities."
              className={errors.description ? 'error' : ''}
              disabled={isSubmitting}
            ></textarea>
            <div className="char-count">
              {jobData.description.length} / 2000 characters
            </div>
            {errors.description && (
              <span className="error-text">
                <i className="fas fa-exclamation-triangle"></i>
                {errors.description}
              </span>
            )}
          </div>

          <div className="form-group full-width">
            <label htmlFor="skills">
              Required Skills
              <span className="required">*</span>
            </label>
            <textarea
              id="skills"
              name="skills"
              value={jobData.skills}
              onChange={handleChange}
              rows="4"
              placeholder="List required skills separated by commas. Example: Python, Django, PostgreSQL, REST APIs, Git, Docker"
              className={errors.skills ? 'error' : ''}
              disabled={isSubmitting}
            ></textarea>
            <div className="skill-preview">
              <p>Skills preview:</p>
              <div className="skills-list">
                {jobData.skills
                  .split(',')
                  .filter(skill => skill.trim())
                  .map((skill, index) => (
                    <span key={index} className="skill-tag">
                      {skill.trim()}
                    </span>
                  ))}
              </div>
            </div>
            {errors.skills && (
              <span className="error-text">
                <i className="fas fa-exclamation-triangle"></i>
                {errors.skills}
              </span>
            )}
          </div>
        </div>

        <div className="form-actions">
          <button 
            type="button" 
            className="btn-secondary"
            onClick={handleReset}
            disabled={isSubmitting}
          >
            <i className="fas fa-redo"></i>
            Clear Form
          </button>
          <button 
            type="submit" 
            className="btn-primary"
            disabled={isSubmitting}
          >
            {isSubmitting ? (
              <>
                <i className="fas fa-spinner fa-spin"></i>
                Posting Job...
              </>
            ) : (
              <>
                <i className="fas fa-paper-plane"></i>
                Post Job
              </>
            )}
          </button>
        </div>
      </form>

      <div className="ai-tips-section">
        <h3>
          <i className="fas fa-lightbulb"></i>
          AI Tips for Better Candidate Matching
        </h3>
        <div className="tips-grid">
          <div className="tip-card">
            <i className="fas fa-check-circle"></i>
            <h4>Be Specific with Skills</h4>
            <p>List exact technologies and tools required. This helps AI match candidates more accurately.</p>
          </div>
          <div className="tip-card">
            <i className="fas fa-check-circle"></i>
            <h4>Clear Job Description</h4>
            <p>Write detailed descriptions of responsibilities. More context helps AI understand the role better.</p>
          </div>
          <div className="tip-card">
            <i className="fas fa-check-circle"></i>
            <h4>Include Experience Level</h4>
            <p>Specify years of experience needed. This helps filter candidates at the right level.</p>
          </div>
          <div className="tip-card">
            <i className="fas fa-check-circle"></i>
            <h4>Mention Nice-to-Have Skills</h4>
            <p>Include optional skills that would be beneficial. AI will identify candidates with these bonuses.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PostJob;
