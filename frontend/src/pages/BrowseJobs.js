import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { jobsAPI, handleApiError } from '../utils/api';
import '../styles/BrowseJobs.css';

const BrowseJobs = () => {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState([]);
  const [filteredJobs, setFilteredJobs] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedJob, setSelectedJob] = useState(null);
  const [filters, setFilters] = useState({
    location: '',
    jobType: '',
    experience: ''
  });

  useEffect(() => {
    fetchJobs();
  }, []);

  useEffect(() => {
    filterJobs();
  }, [searchTerm, filters, jobs]);

  const fetchJobs = async () => {
    try {
      setIsLoading(true);
      const response = await jobsAPI.getAllJobs();
      
      let jobsData = [];
      if (response.data && response.data.jobs) {
        jobsData = response.data.jobs;
      } else if (response.jobs) {
        jobsData = response.jobs;
      }
      
      setJobs(jobsData);
      setFilteredJobs(jobsData);
    } catch (error) {
      console.error('Error fetching jobs:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const filterJobs = () => {
    let filtered = jobs;

    if (searchTerm) {
      filtered = filtered.filter(job =>
        job.job_title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        job.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        job.required_skills?.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filters.location) {
      filtered = filtered.filter(job =>
        job.location?.toLowerCase().includes(filters.location.toLowerCase())
      );
    }

    if (filters.jobType) {
      filtered = filtered.filter(job =>
        job.job_type === filters.jobType
      );
    }

    if (filters.experience) {
      filtered = filtered.filter(job =>
        job.experience_required?.includes(filters.experience)
      );
    }

    setFilteredJobs(filtered);
  };

  const handleApply = (jobId) => {
    navigate('/upload-resume', { state: { selectedJobId: jobId } });
  };

  const handleViewDetails = (job) => {
    setSelectedJob(job);
  };

  const closeModal = () => {
    setSelectedJob(null);
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const clearFilters = () => {
    setSearchTerm('');
    setFilters({
      location: '',
      jobType: '',
      experience: ''
    });
  };

  if (isLoading) {
    return (
      <div className="browse-jobs-loading">
        <i className="fas fa-spinner fa-spin"></i>
        <h3>Loading Jobs...</h3>
      </div>
    );
  }

  return (
    <div className="browse-jobs-container">
      <div className="page-header">
        <div className="header-content">
          <h1>
            <i className="fas fa-search"></i>
            Browse Jobs
          </h1>
          <p>Find your perfect job match with AI-powered recommendations</p>
        </div>
      </div>

      <div className="search-filter-section">
        <div className="search-bar">
          <i className="fas fa-search"></i>
          <input
            type="text"
            placeholder="Search by job title, skills, or description..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <div className="filters">
          <div className="filter-group">
            <label>Location</label>
            <input
              type="text"
              name="location"
              placeholder="Any location"
              value={filters.location}
              onChange={handleFilterChange}
            />
          </div>

          <div className="filter-group">
            <label>Job Type</label>
            <select
              name="jobType"
              value={filters.jobType}
              onChange={handleFilterChange}
            >
              <option value="">All Types</option>
              <option value="full-time">Full Time</option>
              <option value="part-time">Part Time</option>
              <option value="contract">Contract</option>
              <option value="internship">Internship</option>
            </select>
          </div>

          <div className="filter-group">
            <label>Experience</label>
            <select
              name="experience"
              value={filters.experience}
              onChange={handleFilterChange}
            >
              <option value="">All Levels</option>
              <option value="0-1">0-1 years</option>
              <option value="1-3">1-3 years</option>
              <option value="3-5">3-5 years</option>
              <option value="5-10">5-10 years</option>
              <option value="10+">10+ years</option>
            </select>
          </div>

          <button className="clear-filters-btn" onClick={clearFilters}>
            <i className="fas fa-times"></i>
            Clear
          </button>
        </div>
      </div>

      <div className="jobs-results">
        <div className="results-header">
          <h3>
            {filteredJobs.length} {filteredJobs.length === 1 ? 'Job' : 'Jobs'} Found
          </h3>
        </div>

        {filteredJobs.length === 0 ? (
          <div className="no-jobs">
            <i className="fas fa-briefcase"></i>
            <h3>No Jobs Found</h3>
            <p>Try adjusting your search or filters</p>
            <button className="btn-primary" onClick={clearFilters}>
              Clear Filters
            </button>
          </div>
        ) : (
          <div className="jobs-grid">
            {filteredJobs.map((job) => (
              <div key={job._id || job.job_id} className="job-card">
                <div className="job-header">
                  <div className="job-title-section">
                    <h3>{job.job_title || job.title}</h3>
                    <p className="job-department">{job.department || 'Company'}</p>
                  </div>
                  <div className="job-type-badge">
                    {job.job_type || 'Full Time'}
                  </div>
                </div>

                <div className="job-meta">
                  <div className="meta-item">
                    <i className="fas fa-map-marker-alt"></i>
                    <span>{job.location || 'Not specified'}</span>
                  </div>
                  <div className="meta-item">
                    <i className="fas fa-briefcase"></i>
                    <span>{job.experience_required || 'Any'}</span>
                  </div>
                  {job.salary && (
                    <div className="meta-item">
                      <i className="fas fa-dollar-sign"></i>
                      <span>{job.salary}</span>
                    </div>
                  )}
                </div>

                <div className="job-description">
                  <p>{job.description?.substring(0, 150)}...</p>
                </div>

                <div className="job-skills">
                  {(typeof job.required_skills === 'string' 
                    ? job.required_skills.split(',') 
                    : job.required_skills || []
                  ).slice(0, 5).map((skill, index) => (
                    <span key={index} className="skill-tag">
                      {typeof skill === 'string' ? skill.trim() : skill}
                    </span>
                  ))}
                </div>

                <div className="job-footer">
                  <button 
                    className="btn-apply"
                    onClick={() => handleApply(job._id || job.job_id)}
                  >
                    <i className="fas fa-paper-plane"></i>
                    Apply Now
                  </button>
                  <button 
                    className="btn-details"
                    onClick={() => handleViewDetails(job)}
                  >
                    <i className="fas fa-info-circle"></i>
                    View Details
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {selectedJob && (
        <div className="job-modal-overlay" onClick={closeModal}>
          <div className="job-modal" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={closeModal}>
              <i className="fas fa-times"></i>
            </button>
            
            <div className="modal-header">
              <h2>{selectedJob.job_title || selectedJob.title}</h2>
              <span className="job-type-badge">{selectedJob.job_type || 'Full Time'}</span>
            </div>

            <div className="modal-body">
              <div className="modal-section">
                <h3><i className="fas fa-building"></i> Company</h3>
                <p>{selectedJob.department || 'Company Name'}</p>
              </div>

              <div className="modal-section">
                <h3><i className="fas fa-map-marker-alt"></i> Location</h3>
                <p>{selectedJob.location || 'Not specified'}</p>
              </div>

              <div className="modal-section">
                <h3><i className="fas fa-briefcase"></i> Experience Required</h3>
                <p>{selectedJob.experience_required || 'Any level'}</p>
              </div>

              {selectedJob.salary && (
                <div className="modal-section">
                  <h3><i className="fas fa-dollar-sign"></i> Salary</h3>
                  <p>{selectedJob.salary}</p>
                </div>
              )}

              <div className="modal-section">
                <h3><i className="fas fa-align-left"></i> Job Description</h3>
                <p>{selectedJob.description}</p>
              </div>

              <div className="modal-section">
                <h3><i className="fas fa-code"></i> Required Skills</h3>
                <div className="job-skills">
                  {(typeof selectedJob.required_skills === 'string' 
                    ? selectedJob.required_skills.split(',') 
                    : selectedJob.required_skills || []
                  ).map((skill, index) => (
                    <span key={index} className="skill-tag">
                      {typeof skill === 'string' ? skill.trim() : skill}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <div className="modal-footer">
              <button 
                className="btn-apply"
                onClick={() => {
                  closeModal();
                  handleApply(selectedJob._id || selectedJob.job_id);
                }}
              >
                <i className="fas fa-paper-plane"></i>
                Apply Now
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BrowseJobs;
