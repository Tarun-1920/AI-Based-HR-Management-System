import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { candidatesAPI, jobsAPI, handleApiError } from '../utils/api';
import '../styles/UploadResume.css';

const UploadResume = () => {
  const location = useLocation();
  const preSelectedJobId = location.state?.selectedJobId;
  
  const [candidateData, setCandidateData] = useState({
    firstName: '',
    lastName: '',
    email: localStorage.getItem('userEmail') || localStorage.getItem('userName') || '',
    phone: '',
    experience: '',
    expectedSalary: '',
    location: '',
    selectedJob: preSelectedJobId || ''
  });

  const [resumeFile, setResumeFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');
  const [uploadProgress, setUploadProgress] = useState(0);
  const [errors, setErrors] = useState({});
  const [successMessage, setSuccessMessage] = useState('');
  const [showSuccess, setShowSuccess] = useState(false);
  const [jobs, setJobs] = useState([]);
  const [isLoadingJobs, setIsLoadingJobs] = useState(true);

  // Fetch jobs on component mount
  useEffect(() => {
    const fetchJobs = async () => {
      try {
        setIsLoadingJobs(true);
        const response = await jobsAPI.getAllJobs();
        console.log('Full API response:', response);
        
        let jobsData = [];
        if (response.data && response.data.jobs) {
          jobsData = response.data.jobs;
        } else if (response.jobs) {
          jobsData = response.jobs;
        }
        
        console.log('Extracted jobs:', jobsData);
        
        const jobsList = jobsData.map(job => ({
          id: job._id || job.job_id,
          title: job.job_title || job.title,
          company: job.department || 'Company',
          location: job.location || ''
        }));
        
        console.log('Final jobs list:', jobsList);
        setJobs(jobsList);
      } catch (error) {
        console.error('Error fetching jobs:', error);
        setErrors(prev => ({
          ...prev,
          jobsFetch: 'Failed to load jobs. Please refresh the page.'
        }));
        setJobs([]);
      } finally {
        setIsLoadingJobs(false);
      }
    };

    fetchJobs();
  }, []);

  const validateForm = () => {
    const newErrors = {};

    if (!candidateData.firstName.trim()) {
      newErrors.firstName = 'First name is required';
    }
    if (!candidateData.lastName.trim()) {
      newErrors.lastName = 'Last name is required';
    }
    if (!candidateData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(candidateData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }
    if (!resumeFile) {
      newErrors.resume = 'Resume file is required';
    }
    if (!candidateData.selectedJob) {
      newErrors.selectedJob = 'Please select a job position';
    }

    return newErrors;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCandidateData(prev => ({
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

  const handleFileSelect = (file) => {
    if (file && (file.type === 'application/pdf' || file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')) {
      if (file.size > 10 * 1024 * 1024) {
        setErrors(prev => ({
          ...prev,
          resume: 'File size must be less than 10MB'
        }));
        return;
      }
      setResumeFile(file);
      setErrors(prev => ({
        ...prev,
        resume: ''
      }));
    } else {
      setErrors(prev => ({
        ...prev,
        resume: 'Please upload only PDF or DOCX files'
      }));
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const newErrors = validateForm();
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setIsUploading(true);
    setUploadStatus('Uploading resume...');
    setUploadProgress(0);

    try {
      // Prepare form data
      const formData = new FormData();
      formData.append('firstName', candidateData.firstName);
      formData.append('lastName', candidateData.lastName);
      formData.append('email', candidateData.email);
      formData.append('phone', candidateData.phone);
      formData.append('experience', candidateData.experience);
      formData.append('expectedSalary', candidateData.expectedSalary);
      formData.append('location', candidateData.location);
      formData.append('jobId', candidateData.selectedJob);
      formData.append('resume', resumeFile);

      // Call API to upload resume
      await candidatesAPI.uploadResume(formData, (progress) => {
        setUploadProgress(progress);
        
        if (progress < 30) {
          setUploadStatus('Uploading resume...');
        } else if (progress < 70) {
          setUploadStatus('Analyzing resume with AI...');
        } else {
          setUploadStatus('Finding matching jobs...');
        }
      });

      setUploadProgress(100);
      setUploadStatus('Processing complete!');

      // Dispatch event to refresh dashboard
      window.dispatchEvent(new Event('resumeUploaded'));

      // Success
      const selectedJobTitle = jobs.find(job => job.id === candidateData.selectedJob)?.title;
      setSuccessMessage(
        `Resume submitted successfully! Your application for "${selectedJobTitle}" has been received. Our AI is analyzing your profile.`
      );
      setShowSuccess(true);

      // Reset form
      setCandidateData({
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        experience: '',
        expectedSalary: '',
        location: '',
        selectedJob: ''
      });
      setResumeFile(null);
      setUploadProgress(0);
      setUploadStatus('');

      // Hide success message after 6 seconds
      setTimeout(() => {
        setShowSuccess(false);
      }, 6000);

    } catch (error) {
      const errorMsg = handleApiError(error);
      setErrors({ submit: errorMsg });
    } finally {
      setIsUploading(false);
    }
  };

  const handleReset = () => {
    setCandidateData({
      firstName: '',
      lastName: '',
      email: '',
      phone: '',
      experience: '',
      expectedSalary: '',
      location: '',
      selectedJob: ''
    });
    setResumeFile(null);
    setErrors({});
    setShowSuccess(false);
    setUploadProgress(0);
    setUploadStatus('');
  };

  const getSelectedJobDetails = () => {
    return jobs.find(job => job.id === candidateData.selectedJob);
  };

  return (
    <div className="upload-resume-container">
      <div className="page-header">
        <div className="header-content">
          <h1>
            <i className="fas fa-upload"></i>
            Upload Your Resume
          </h1>
          <p>Let our AI analyze your skills and match you with perfect job opportunities</p>
        </div>
        <div className="header-icon">
          <i className="fas fa-file-upload"></i>
        </div>
      </div>

      {showSuccess && (
        <div className="success-message">
          <div className="success-content">
            <i className="fas fa-check-circle"></i>
            <div>
              <h3>Application Submitted Successfully!</h3>
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

      {errors.submit && (
        <div className="error-message">
          <i className="fas fa-exclamation-circle"></i>
          <span>{errors.submit}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="resume-form">
        {/* Personal Information Section */}
        <div className="form-section">
          <div className="section-header">
            <h2>
              <i className="fas fa-user"></i>
              Personal Information
            </h2>
            <p>Tell us about yourself</p>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="firstName">
                First Name
                <span className="required">*</span>
              </label>
              <input
                type="text"
                id="firstName"
                name="firstName"
                value={candidateData.firstName}
                onChange={handleChange}
                placeholder="John"
                className={errors.firstName ? 'error' : ''}
                disabled={isUploading}
              />
              {errors.firstName && (
                <span className="error-text">
                  <i className="fas fa-exclamation-triangle"></i>
                  {errors.firstName}
                </span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="lastName">
                Last Name
                <span className="required">*</span>
              </label>
              <input
                type="text"
                id="lastName"
                name="lastName"
                value={candidateData.lastName}
                onChange={handleChange}
                placeholder="Doe"
                className={errors.lastName ? 'error' : ''}
                disabled={isUploading}
              />
              {errors.lastName && (
                <span className="error-text">
                  <i className="fas fa-exclamation-triangle"></i>
                  {errors.lastName}
                </span>
              )}
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="email">
                Email Address
                <span className="required">*</span>
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={candidateData.email}
                onChange={handleChange}
                placeholder="john.doe@email.com"
                className={errors.email ? 'error' : ''}
                disabled={isUploading}
                readOnly
              />
              {errors.email && (
                <span className="error-text">
                  <i className="fas fa-exclamation-triangle"></i>
                  {errors.email}
                </span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="phone">
                Phone Number
              </label>
              <input
                type="tel"
                id="phone"
                name="phone"
                value={candidateData.phone}
                onChange={handleChange}
                placeholder="+1 (555) 123-4567"
                disabled={isUploading}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="experience">
                Years of Experience
              </label>
              <select
                id="experience"
                name="experience"
                value={candidateData.experience}
                onChange={handleChange}
                disabled={isUploading}
              >
                <option value="">Select experience level</option>
                <option value="0-1">0-1 years (Fresher)</option>
                <option value="1-3">1-3 years</option>
                <option value="3-5">3-5 years</option>
                <option value="5-10">5-10 years</option>
                <option value="10+">10+ years</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="location">
                Preferred Location
              </label>
              <input
                type="text"
                id="location"
                name="location"
                value={candidateData.location}
                onChange={handleChange}
                placeholder="e.g. New York, NY / Remote"
                disabled={isUploading}
              />
            </div>
          </div>

          <div className="form-group full-width">
            <label htmlFor="expectedSalary">
              Expected Salary
            </label>
            <input
              type="text"
              id="expectedSalary"
              name="expectedSalary"
              value={candidateData.expectedSalary}
              onChange={handleChange}
              placeholder="e.g. $70,000 - $90,000"
              disabled={isUploading}
            />
          </div>
        </div>

        {/* Job Selection Section */}
        <div className="form-section">
          <div className="section-header">
            <h2>
              <i className="fas fa-briefcase"></i>
              Select Job Position
            </h2>
            <p>Choose the position you want to apply for</p>
          </div>

          <div className="form-group full-width">
            <label htmlFor="selectedJob">
              Job Position
              <span className="required">*</span>
            </label>
            {isLoadingJobs ? (
              <div className="loading-jobs">
                <i className="fas fa-spinner fa-spin"></i>
                <span>Loading available positions...</span>
              </div>
            ) : jobs.length === 0 ? (
              <div className="no-jobs-message">
                <i className="fas fa-info-circle"></i>
                <span>No job positions available at the moment. Please check back later.</span>
              </div>
            ) : (
              <select
                id="selectedJob"
                name="selectedJob"
                value={candidateData.selectedJob}
                onChange={handleChange}
                className={errors.selectedJob ? 'error' : ''}
                disabled={isUploading}
              >
                <option value="">-- Select a job position --</option>
                {jobs.map(job => (
                  <option key={job.id} value={job.id}>
                    {job.title} {job.location ? `- ${job.location}` : ''}
                  </option>
                ))}
              </select>
            )}
            {errors.selectedJob && (
              <span className="error-text">
                <i className="fas fa-exclamation-triangle"></i>
                {errors.selectedJob}
              </span>
            )}
            {errors.jobsFetch && (
              <span className="error-text">
                <i className="fas fa-exclamation-triangle"></i>
                {errors.jobsFetch}
              </span>
            )}
          </div>

          {candidateData.selectedJob && getSelectedJobDetails() && (
            <div className="job-preview">
              <div className="job-preview-content">
                <i className="fas fa-star"></i>
                <div>
                  <h4>{getSelectedJobDetails().title}</h4>
                  <p>{getSelectedJobDetails().company}</p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Resume Upload Section */}
        <div className="form-section">
          <div className="section-header">
            <h2>
              <i className="fas fa-file-alt"></i>
              Upload Resume
            </h2>
            <p>Drag and drop or click to upload your resume</p>
          </div>

          <div 
            className={`file-upload-area ${dragActive ? 'drag-active' : ''} ${resumeFile ? 'has-file' : ''}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            {resumeFile ? (
              <div className="file-selected">
                <div className="file-icon">
                  <i className={resumeFile.type === 'application/pdf' ? 'fas fa-file-pdf' : 'fas fa-file-word'}></i>
                </div>
                <div className="file-info">
                  <h4>{resumeFile.name}</h4>
                  <p>{(resumeFile.size / 1024 / 1024).toFixed(2)} MB</p>
                  <span className="file-type">
                    {resumeFile.type === 'application/pdf' ? 'PDF Document' : 'Word Document'}
                  </span>
                </div>
                <button 
                  type="button" 
                  className="remove-file"
                  onClick={() => setResumeFile(null)}
                  disabled={isUploading}
                >
                  <i className="fas fa-times"></i>
                </button>
              </div>
            ) : (
              <div className="upload-prompt">
                <i className="fas fa-cloud-upload-alt"></i>
                <h4>Drag your resume here</h4>
                <p>or click to browse files</p>
                <p className="file-types">Supported formats: PDF, DOCX (Max 10MB)</p>
              </div>
            )}
            <input
              type="file"
              accept=".pdf,.docx"
              onChange={handleFileInput}
              style={{ display: 'none' }}
              id="resume-upload"
              disabled={isUploading}
            />
            <label htmlFor="resume-upload" className="file-input-label"></label>
          </div>

          {errors.resume && (
            <span className="error-text">
              <i className="fas fa-exclamation-triangle"></i>
              {errors.resume}
            </span>
          )}

          {isUploading && (
            <div className="upload-progress">
              <div className="progress-bar">
                <div className="progress-fill" style={{ width: `${uploadProgress}%` }}></div>
              </div>
              <div className="progress-info">
                <span className="progress-text">{uploadStatus}</span>
                <span className="progress-percent">{Math.round(uploadProgress)}%</span>
              </div>
            </div>
          )}
        </div>

        {/* AI Features Section */}
        <div className="ai-features">
          <h3><i className="fas fa-brain"></i> What Our AI Will Analyze</h3>
          <div className="features-grid">
            <div className="feature-item">
              <i className="fas fa-cogs"></i>
              <span>Technical Skills</span>
            </div>
            <div className="feature-item">
              <i className="fas fa-graduation-cap"></i>
              <span>Education & Certifications</span>
            </div>
            <div className="feature-item">
              <i className="fas fa-briefcase"></i>
              <span>Work Experience</span>
            </div>
            <div className="feature-item">
              <i className="fas fa-project-diagram"></i>
              <span>Projects & Achievements</span>
            </div>
            <div className="feature-item">
              <i className="fas fa-language"></i>
              <span>Languages & Tools</span>
            </div>
            <div className="feature-item">
              <i className="fas fa-chart-line"></i>
              <span>Career Growth</span>
            </div>
          </div>
        </div>

        {/* Form Actions */}
        <div className="form-actions">
          <button 
            type="button" 
            className="btn-secondary"
            onClick={handleReset}
            disabled={isUploading}
          >
            <i className="fas fa-redo"></i>
            Clear Form
          </button>
          <button 
            type="submit" 
            className="btn-primary"
            disabled={isUploading}
          >
            {isUploading ? (
              <>
                <i className="fas fa-spinner fa-spin"></i>
                Uploading...
              </>
            ) : (
              <>
                <i className="fas fa-paper-plane"></i>
                Submit Application
              </>
            )}
          </button>
        </div>
      </form>

      {/* Tips Section */}
      <div className="tips-section">
        <h3>
          <i className="fas fa-lightbulb"></i>
          Tips for Better AI Matching
        </h3>
        <div className="tips-grid">
          <div className="tip-card">
            <i className="fas fa-check-circle"></i>
            <h4>Use Clear Formatting</h4>
            <p>Use standard resume formatting with clear sections. This helps AI extract information accurately.</p>
          </div>
          <div className="tip-card">
            <i className="fas fa-check-circle"></i>
            <h4>Include All Skills</h4>
            <p>List all technical and soft skills. Be specific about tools, languages, and frameworks you know.</p>
          </div>
          <div className="tip-card">
            <i className="fas fa-check-circle"></i>
            <h4>Highlight Achievements</h4>
            <p>Include quantifiable achievements and results. This helps AI understand your impact and value.</p>
          </div>
          <div className="tip-card">
            <i className="fas fa-check-circle"></i>
            <h4>Keep It Updated</h4>
            <p>Ensure your resume is current with recent experience and skills. Remove outdated information.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UploadResume;
