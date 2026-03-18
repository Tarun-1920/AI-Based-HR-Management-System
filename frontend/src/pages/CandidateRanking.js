import React, { useState, useEffect } from 'react';
import { candidatesAPI, jobsAPI, handleApiError } from '../utils/api';
import '../styles/CandidateRanking.css';

const CandidateRanking = () => {
  const [candidates, setCandidates] = useState([]);
  const [filteredCandidates, setFilteredCandidates] = useState([]);
  const [sortBy, setSortBy] = useState('matchScore');
  const [sortOrder, setSortOrder] = useState('desc');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedJob, setSelectedJob] = useState('all');
  const [selectedStatus, setSelectedStatus] = useState('all');
  const [jobs, setJobs] = useState([{ id: 'all', title: 'All Jobs' }]);

  // Mock candidate data
  const mockCandidates = [
    {
      id: 1,
      name: 'Alice Johnson',
      email: 'alice.johnson@email.com',
      jobId: 1,
      jobTitle: 'Senior Python Developer',
      skills: ['Python', 'Django', 'PostgreSQL', 'REST APIs', 'Git', 'Docker'],
      matchScore: 95,
      status: 'shortlisted',
      appliedDate: '2024-01-15',
      resumeUrl: '/resumes/alice_johnson.pdf'
    },
    {
      id: 2,
      name: 'Robert Smith',
      email: 'robert.smith@email.com',
      jobId: 2,
      jobTitle: 'Data Analyst',
      skills: ['Python', 'SQL', 'Tableau', 'Excel', 'Statistics', 'R'],
      matchScore: 88,
      status: 'reviewed',
      appliedDate: '2024-01-14',
      resumeUrl: '/resumes/robert_smith.pdf'
    },
    {
      id: 3,
      name: 'Emily Davis',
      email: 'emily.davis@email.com',
      jobId: 3,
      jobTitle: 'Full Stack Developer',
      skills: ['React', 'Node.js', 'MongoDB', 'TypeScript', 'CSS', 'JavaScript'],
      matchScore: 87,
      status: 'shortlisted',
      appliedDate: '2024-01-13',
      resumeUrl: '/resumes/emily_davis.pdf'
    },
    {
      id: 4,
      name: 'David Wilson',
      email: 'david.wilson@email.com',
      jobId: 1,
      jobTitle: 'Senior Python Developer',
      skills: ['Python', 'Flask', 'MySQL', 'Docker', 'AWS', 'Linux'],
      matchScore: 82,
      status: 'new',
      appliedDate: '2024-01-12',
      resumeUrl: '/resumes/david_wilson.pdf'
    },
    {
      id: 5,
      name: 'Sarah Martinez',
      email: 'sarah.martinez@email.com',
      jobId: 4,
      jobTitle: 'DevOps Engineer',
      skills: ['AWS', 'Docker', 'Kubernetes', 'Jenkins', 'Python', 'Terraform'],
      matchScore: 91,
      status: 'shortlisted',
      appliedDate: '2024-01-11',
      resumeUrl: '/resumes/sarah_martinez.pdf'
    },
    {
      id: 6,
      name: 'Michael Chen',
      email: 'michael.chen@email.com',
      jobId: 5,
      jobTitle: 'React Frontend Developer',
      skills: ['React', 'JavaScript', 'CSS', 'HTML', 'Redux', 'Webpack'],
      matchScore: 79,
      status: 'rejected',
      appliedDate: '2024-01-10',
      resumeUrl: '/resumes/michael_chen.pdf'
    },
    {
      id: 7,
      name: 'Jessica Brown',
      email: 'jessica.brown@email.com',
      jobId: 2,
      jobTitle: 'Data Analyst',
      skills: ['SQL', 'Python', 'Power BI', 'Excel', 'Statistics'],
      matchScore: 85,
      status: 'reviewed',
      appliedDate: '2024-01-09',
      resumeUrl: '/resumes/jessica_brown.pdf'
    },
    {
      id: 8,
      name: 'James Taylor',
      email: 'james.taylor@email.com',
      jobId: 3,
      jobTitle: 'Full Stack Developer',
      skills: ['Vue.js', 'Node.js', 'PostgreSQL', 'JavaScript', 'HTML', 'CSS'],
      matchScore: 80,
      status: 'new',
      appliedDate: '2024-01-08',
      resumeUrl: '/resumes/james_taylor.pdf'
    }
  ];

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const jobsResponse = await jobsAPI.getAllJobs();
        
        let jobsList = [];
        if (jobsResponse.data && jobsResponse.data.jobs) {
          jobsList = jobsResponse.data.jobs;
        } else if (jobsResponse.jobs) {
          jobsList = jobsResponse.jobs;
        }
        
        const formattedJobs = [
          { id: 'all', title: 'All Jobs' },
          ...jobsList.map(job => ({
            id: job._id || job.job_id,
            title: job.job_title || job.title
          }))
        ];
        
        setJobs(formattedJobs);
      } catch (error) {
        console.error('Error fetching jobs:', error);
      }
    };
    
    fetchJobs();
  }, []);

  useEffect(() => {
    const fetchCandidates = async () => {
      try {
        const response = await candidatesAPI.getAllCandidates();
        console.log('Candidates response:', response);
        
        const candidatesList = (response.candidates || []).map(candidate => ({
          id: candidate.candidate_id || candidate._id,
          name: candidate.candidate_name || candidate.name,
          email: candidate.email,
          jobId: candidate.job_id,
          jobTitle: candidate.job_applied || 'N/A',
          skills: candidate.skills || [],
          matchScore: candidate.match_score || 0,
          status: candidate.status || 'pending',
          appliedDate: candidate.applied_at || new Date().toISOString(),
          resumeUrl: candidate.resume_file || ''
        }));
        
        console.log('Mapped candidates:', candidatesList);
        setCandidates(candidatesList);
        filterAndSortCandidates(candidatesList);
      } catch (error) {
        console.error('Error fetching candidates:', error);
        setCandidates([]);
        setFilteredCandidates([]);
      }
    };
    
    fetchCandidates();
  }, []);

  const filterAndSortCandidates = (data) => {
    let filtered = data;

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(candidate =>
        candidate.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        candidate.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
        candidate.skills.some(skill => skill.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    // Filter by job
    if (selectedJob !== 'all') {
      filtered = filtered.filter(candidate => {
        const candidateJobId = String(candidate.jobId);
        const selectedJobId = String(selectedJob);
        return candidateJobId === selectedJobId;
      });
    }

    // Filter by status
    if (selectedStatus !== 'all') {
      filtered = filtered.filter(candidate => candidate.status === selectedStatus);
    }

    // Sort candidates
    filtered.sort((a, b) => {
      let aValue, bValue;

      switch (sortBy) {
        case 'matchScore':
          aValue = a.matchScore;
          bValue = b.matchScore;
          break;
        case 'name':
          aValue = a.name.toLowerCase();
          bValue = b.name.toLowerCase();
          break;
        case 'date':
          aValue = new Date(a.appliedDate);
          bValue = new Date(b.appliedDate);
          break;
        default:
          aValue = a.matchScore;
          bValue = b.matchScore;
      }

      if (sortOrder === 'asc') {
        return aValue > bValue ? 1 : -1;
      } else {
        return aValue < bValue ? 1 : -1;
      }
    });

    setFilteredCandidates(filtered);
  };

  useEffect(() => {
    filterAndSortCandidates(candidates);
  }, [searchTerm, selectedJob, selectedStatus, sortBy, sortOrder]);

  const handleSort = (column) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(column);
      setSortOrder('desc');
    }
  };

  const handleDownloadResume = async (candidateId, candidateName) => {
    try {
      const blob = await candidatesAPI.downloadResume(candidateId);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${candidateName.replace(/\s+/g, '_')}_Resume.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error downloading resume:', error);
      alert('Failed to download resume. File may not be available.');
    }
  };

  const handleStatusChange = async (candidateId, newStatus) => {
    try {
      await candidatesAPI.updateCandidateStatus(candidateId, newStatus);
      
      setCandidates(prev =>
        prev.map(candidate =>
          candidate.id === candidateId
            ? { ...candidate, status: newStatus }
            : candidate
        )
      );
    } catch (error) {
      console.error('Error updating status:', error);
      alert('Failed to update candidate status');
    }
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'pending':
      case 'new': return '#3498db';
      case 'reviewed': return '#f39c12';
      case 'shortlisted': return '#27ae60';
      case 'interviewed': return '#9b59b6';
      case 'hired': return '#2ecc71';
      case 'rejected': return '#e74c3c';
      default: return '#95a5a6';
    }
  };

  const getMatchScoreColor = (score) => {
    if (score >= 90) return '#27ae60';
    if (score >= 80) return '#f39c12';
    if (score >= 70) return '#e67e22';
    return '#e74c3c';
  };

  const getSortIcon = (column) => {
    if (sortBy !== column) return 'fas fa-sort';
    return sortOrder === 'asc' ? 'fas fa-sort-up' : 'fas fa-sort-down';
  };

  return (
    <div className="candidate-ranking-container">
      <div className="page-header">
        <div className="header-content">
          <h1>
            <i className="fas fa-ranking-star"></i>
            Candidate Ranking
          </h1>
          <p>AI-powered candidate ranking and management system</p>
        </div>
        <div className="header-stats">
          <div className="stat">
            <span className="stat-number">{filteredCandidates.length}</span>
            <span className="stat-label">Candidates</span>
          </div>
          <div className="stat">
            <span className="stat-number">
              {filteredCandidates.filter(c => c.matchScore >= 80).length}
            </span>
            <span className="stat-label">High Match</span>
          </div>
          <div className="stat">
            <span className="stat-number">
              {filteredCandidates.filter(c => c.status === 'shortlisted').length}
            </span>
            <span className="stat-label">Shortlisted</span>
          </div>
        </div>
      </div>

      {/* Filters Section */}
      <div className="filters-section">
        <div className="search-bar">
          <i className="fas fa-search"></i>
          <input
            type="text"
            placeholder="Search by name, email, or skills..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <div className="filter-controls">
          <div className="filter-group">
            <label>Job Position:</label>
            <select value={selectedJob} onChange={(e) => setSelectedJob(e.target.value)}>
              {jobs.map(job => (
                <option key={job.id} value={job.id}>{job.title}</option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label>Status:</label>
            <select value={selectedStatus} onChange={(e) => setSelectedStatus(e.target.value)}>
              <option value="all">All Status</option>
              <option value="pending">New/Pending</option>
              <option value="reviewed">Reviewed</option>
              <option value="shortlisted">Shortlisted</option>
              <option value="interviewed">Interviewed</option>
              <option value="hired">Hired</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>
        </div>
      </div>

      {/* Candidates Table */}
      <div className="table-container">
        <table className="candidates-table">
          <thead>
            <tr>
              <th onClick={() => handleSort('name')}>
                <span>Candidate Name</span>
                <i className={getSortIcon('name')}></i>
              </th>
              <th>Email</th>
              <th>Applied Job</th>
              <th>Skills</th>
              <th onClick={() => handleSort('matchScore')}>
                <span>Match Score</span>
                <i className={getSortIcon('matchScore')}></i>
              </th>
              <th>Resume</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredCandidates.length > 0 ? (
              filteredCandidates.map(candidate => (
                <tr key={candidate.id} className="candidate-row">
                  <td className="name-cell">
                    <div className="candidate-avatar">
                      {candidate.name.split(' ').map(n => n[0]).join('')}
                    </div>
                    <span>{candidate.name}</span>
                  </td>
                  <td className="email-cell">
                    <a href={`mailto:${candidate.email}`}>{candidate.email}</a>
                  </td>
                  <td className="job-cell">{candidate.jobTitle}</td>
                  <td className="skills-cell">
                    <div className="skills-container">
                      {candidate.skills.slice(0, 3).map(skill => (
                        <span key={skill} className="skill-badge">{skill}</span>
                      ))}
                      {candidate.skills.length > 3 && (
                        <span className="skill-more">+{candidate.skills.length - 3}</span>
                      )}
                    </div>
                  </td>
                  <td className="score-cell">
                    <div className="match-score-container">
                      <div className="score-value" style={{ color: getMatchScoreColor(candidate.matchScore) }}>
                        {candidate.matchScore}%
                      </div>
                      <div className="progress-bar">
                        <div 
                          className="progress-fill" 
                          style={{ 
                            width: `${candidate.matchScore}%`,
                            backgroundColor: getMatchScoreColor(candidate.matchScore)
                          }}
                        ></div>
                      </div>
                    </div>
                  </td>
                  <td className="resume-cell">
                    <button 
                      className="download-btn" 
                      title="Download Resume"
                      onClick={() => handleDownloadResume(candidate.id, candidate.name)}
                    >
                      <i className="fas fa-download"></i>
                      Download
                    </button>
                  </td>
                  <td className="status-cell">
                    <span 
                      className="status-badge"
                      style={{ backgroundColor: getStatusColor(candidate.status) }}
                    >
                      {candidate.status.charAt(0).toUpperCase() + candidate.status.slice(1)}
                    </span>
                  </td>
                  <td className="actions-cell">
                    <div className="action-buttons">
                      <button 
                        className="action-btn shortlist-btn"
                        onClick={() => handleStatusChange(candidate.id, 'shortlisted')}
                        title="Shortlist"
                        disabled={candidate.status === 'shortlisted'}
                      >
                        <i className="fas fa-check"></i>
                      </button>
                      <button 
                        className="action-btn reject-btn"
                        onClick={() => handleStatusChange(candidate.id, 'rejected')}
                        title="Reject"
                        disabled={candidate.status === 'rejected'}
                      >
                        <i className="fas fa-times"></i>
                      </button>
                      <button 
                        className="action-btn view-btn"
                        title="View Details"
                      >
                        <i className="fas fa-eye"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            ) : (
              <tr className="no-results">
                <td colSpan="8">
                  <div className="no-results-message">
                    <i className="fas fa-search"></i>
                    <p>No candidates found matching your criteria</p>
                  </div>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Summary Section */}
      <div className="summary-section">
        <div className="summary-card">
          <h3>Match Score Distribution</h3>
          <div className="distribution-grid">
            <div className="distribution-item">
              <span className="label">90-100%</span>
              <span className="count">{candidates.filter(c => c.matchScore >= 90).length}</span>
            </div>
            <div className="distribution-item">
              <span className="label">80-89%</span>
              <span className="count">{candidates.filter(c => c.matchScore >= 80 && c.matchScore < 90).length}</span>
            </div>
            <div className="distribution-item">
              <span className="label">70-79%</span>
              <span className="count">{candidates.filter(c => c.matchScore >= 70 && c.matchScore < 80).length}</span>
            </div>
            <div className="distribution-item">
              <span className="label">Below 70%</span>
              <span className="count">{candidates.filter(c => c.matchScore < 70).length}</span>
            </div>
          </div>
        </div>

        <div className="summary-card">
          <h3>Status Distribution</h3>
          <div className="distribution-grid">
            <div className="distribution-item">
              <span className="label">Pending</span>
              <span className="count">{candidates.filter(c => c.status === 'pending' || c.status === 'new').length}</span>
            </div>
            <div className="distribution-item">
              <span className="label">Reviewed</span>
              <span className="count">{candidates.filter(c => c.status === 'reviewed').length}</span>
            </div>
            <div className="distribution-item">
              <span className="label">Shortlisted</span>
              <span className="count">{candidates.filter(c => c.status === 'shortlisted').length}</span>
            </div>
            <div className="distribution-item">
              <span className="label">Rejected</span>
              <span className="count">{candidates.filter(c => c.status === 'rejected').length}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CandidateRanking;
