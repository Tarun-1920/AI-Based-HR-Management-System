import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { jobsAPI, candidatesAPI } from '../utils/api';
import '../styles/Dashboard.css';

const Dashboard = ({ userRole }) => {
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    totalJobs: 0,
    totalApplicants: 0,
    topCandidateMatch: 0,
    aiProcessingStatus: 'Active'
  });

  const [isLoading, setIsLoading] = useState(true);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [topCandidates, setTopCandidates] = useState([]);
  const [recentActivities, setRecentActivities] = useState([]);
  const [candidateApplications, setCandidateApplications] = useState([]);
  const [profileStatus, setProfileStatus] = useState({
    profileCreated: false,
    resumeUploaded: false,
    skillsVerified: false,
    interviewScheduled: false
  });

  // Simulate loading data
  useEffect(() => {
    const loadDashboardData = async () => {
      setIsLoading(true);
      
      try {
        if (userRole === 'candidate') {
          // Fetch candidate-specific data
          const userEmail = localStorage.getItem('userEmail') || localStorage.getItem('userName');
          console.log('Dashboard - Looking for applications with email:', userEmail);
          
          // Fetch all candidates to find current user's applications
          const candidatesResponse = await candidatesAPI.getAllCandidates();
          
          let candidates = [];
          if (candidatesResponse.data && candidatesResponse.data.candidates) {
            candidates = candidatesResponse.data.candidates;
          } else if (candidatesResponse.candidates) {
            candidates = candidatesResponse.candidates;
          }
          
          // Filter candidates by current user's email
          const userApplications = candidates.filter(c => 
            c.email?.toLowerCase() === userEmail?.toLowerCase()
          );
          
          console.log('User Applications:', userApplications);
          
          // Fetch all jobs to get job details
          const jobsResponse = await jobsAPI.getAllJobs();
          let jobs = [];
          if (jobsResponse.data && jobsResponse.data.jobs) {
            jobs = jobsResponse.data.jobs;
          } else if (jobsResponse.jobs) {
            jobs = jobsResponse.jobs;
          }
          
          // Map applications with job details
          const applicationsWithDetails = userApplications.map(app => {
            const job = jobs.find(j => j._id === app.job_id);
            return {
              id: app._id || app.candidate_id,
              jobTitle: job?.job_title || 'Position',
              company: job?.department || 'Company',
              status: app.status || 'applied',
              matchScore: Math.round(app.match_score || 0),
              appliedDate: app.created_at || new Date().toISOString()
            };
          });
          
          setCandidateApplications(applicationsWithDetails);
          
          // Update stats
          const topMatch = userApplications.length > 0 
            ? Math.max(...userApplications.map(c => c.match_score || 0))
            : 0;
          
          setStats({
            totalJobs: jobs.length,
            totalApplicants: userApplications.length,
            topCandidateMatch: Math.round(topMatch),
            aiProcessingStatus: 'Active'
          });
          
          // Update profile status based on real data
          setProfileStatus({
            profileCreated: true, // User is logged in
            resumeUploaded: userApplications.length > 0,
            skillsVerified: userApplications.some(app => app.skills && app.skills.length > 0),
            interviewScheduled: userApplications.some(app => app.status === 'interviewed')
          });
          
        } else {
          // HR Dashboard - existing logic
          const [jobsResponse, candidatesResponse] = await Promise.all([
            jobsAPI.getAllJobs(),
            candidatesAPI.getAllCandidates()
          ]);
          
          console.log('Jobs Response:', jobsResponse);
          console.log('Candidates Response:', candidatesResponse);
          
          // Parse jobs data
          let jobs = [];
          if (jobsResponse.data && jobsResponse.data.jobs) {
            jobs = jobsResponse.data.jobs;
          } else if (jobsResponse.jobs) {
            jobs = jobsResponse.jobs;
          }
          
          // Parse candidates data
          let candidates = [];
          if (candidatesResponse.data && candidatesResponse.data.candidates) {
            candidates = candidatesResponse.data.candidates;
          } else if (candidatesResponse.candidates) {
            candidates = candidatesResponse.candidates;
          }
          
          console.log('Parsed Jobs:', jobs.length);
          console.log('Parsed Candidates:', candidates.length);
          
          // Debug: Log first candidate and job to see structure
          if (candidates.length > 0) {
            console.log('Sample Candidate:', candidates[0]);
          }
          if (jobs.length > 0) {
            console.log('Sample Job:', jobs[0]);
          }
          
          const topMatch = candidates.length > 0 
            ? Math.max(...candidates.map(c => c.match_score || 0))
            : 0;
          
          const targetStats = {
            totalJobs: jobs.length,
            totalApplicants: candidates.length,
            topCandidateMatch: Math.round(topMatch),
            aiProcessingStatus: 'Active'
          };
          
          setStats(targetStats);
          
          const topCandidatesList = candidates
            .sort((a, b) => (b.match_score || 0) - (a.match_score || 0))
            .slice(0, 4)
            .map(c => {
              // Backend already provides job_applied with the job title
              return {
                id: c.candidate_id || c._id,
                name: c.candidate_name || c.name || 'N/A',
                position: c.job_applied || 'Position Not Found',
                match: Math.round(c.match_score || 0),
                skills: c.skills || [],
                avatar: (c.candidate_name || c.name || 'NA').split(' ').map(n => n[0]).join(''),
                status: c.status || 'pending'
              };
            });
          
          console.log('Top Candidates with positions:', topCandidatesList);
          
          setTopCandidates(topCandidatesList);
          
          // Generate recent activities from real data
          const activities = [];
          candidates.slice(0, 3).forEach((candidate, index) => {
            const job = jobs.find(j => j._id === candidate.job_id);
            const appliedDate = candidate.applied_at || candidate.created_at;
            activities.push({
              id: `app-${index}`,
              action: `New candidate ${candidate.candidate_name || candidate.name || 'Unknown'} applied for ${job?.job_title || 'a position'}`,
              time: appliedDate ? new Date(appliedDate).toLocaleString('en-US', {
                month: 'short',
                day: 'numeric',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
              }) : 'Recently',
              type: 'application',
              user: candidate.candidate_name || candidate.name || 'Candidate'
            });
          });
          
          jobs.slice(0, 2).forEach((job, index) => {
            const postedDate = job.posted_date || job.created_at;
            activities.push({
              id: `job-${index}`,
              action: `Job posted: ${job.job_title}`,
              time: postedDate ? new Date(postedDate).toLocaleString('en-US', {
                month: 'short',
                day: 'numeric',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
              }) : 'Recently',
              type: 'job',
              user: 'HR Manager'
            });
          });
          
          setRecentActivities(activities.slice(0, 5).sort((a, b) => {
            // Sort by most recent first
            const timeA = a.time === 'Recently' ? new Date() : new Date(a.time);
            const timeB = b.time === 'Recently' ? new Date() : new Date(b.time);
            return timeB - timeA;
          }));
        }
      } catch (error) {
        console.error('Error loading dashboard data:', error);
        setStats({
          totalJobs: 0,
          totalApplicants: 0,
          topCandidateMatch: 0,
          aiProcessingStatus: 'Active'
        });
      }
      
      setIsLoading(false);
    };
    
    loadDashboardData();

    // Listen for resume upload event
    const handleResumeUploaded = () => {
      console.log('Resume uploaded event received, refreshing dashboard...');
      loadDashboardData();
    };

    window.addEventListener('resumeUploaded', handleResumeUploaded);

    return () => {
      window.removeEventListener('resumeUploaded', handleResumeUploaded);
    };
  }, [userRole]);

  // Update time every second
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    
    return () => clearInterval(timer);
  }, []);

const aiInsights = [
    {
      title: 'Most In-Demand Skills',
      data: ['Python', 'React', 'AWS', 'SQL', 'Docker'],
      icon: 'fas fa-chart-line',
      color: '#667eea'
    },
    {
      title: 'Average Match Score',
      data: '78%',
      icon: 'fas fa-bullseye',
      color: '#4CAF50'
    },
    {
      title: 'Processing Speed',
      data: '2.3 sec/resume',
      icon: 'fas fa-tachometer-alt',
      color: '#FF9800'
    }
  ];

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'new':
      case 'pending': return '#3498db';
      case 'reviewed': return '#f39c12';
      case 'shortlisted': return '#27ae60';
      case 'interviewed': return '#9b59b6';
      case 'hired': return '#2ecc71';
      case 'rejected': return '#e74c3c';
      default: return '#95a5a6';
    }
  };

  const getActivityIcon = (type) => {
    switch (type) {
      case 'application': return 'fas fa-user-plus';
      case 'match': return 'fas fa-brain';
      case 'job': return 'fas fa-briefcase';
      case 'resume': return 'fas fa-file-alt';
      case 'interview': return 'fas fa-calendar-check';
      default: return 'fas fa-info-circle';
    }
  };

  if (isLoading) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner">
          <i className="fas fa-brain fa-spin"></i>
          <h3>Loading Dashboard...</h3>
          <p>Fetching your AI-powered insights</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      {/* Dashboard Header */}
      <div className="dashboard-header">
        <div className="header-content">
          <div className="welcome-section">
            <h1>
              <i className="fas fa-tachometer-alt"></i>
              {userRole === 'hr' ? 'HR Dashboard' : 'Candidate Dashboard'}
            </h1>
            <p>Welcome back! Here's your AI-powered recruitment overview.</p>
          </div>
          <div className="header-info">
            <div className="time-display">
              <i className="fas fa-clock"></i>
              <span>{currentTime.toLocaleTimeString()}</span>
            </div>
            <div className="date-display">
              <i className="fas fa-calendar"></i>
              <span>{currentTime.toLocaleDateString('en-US', { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
              })}</span>
            </div>
          </div>
        </div>
      </div>

      {userRole === 'hr' ? (
        <>
          {/* Stats Cards */}
          <div className="stats-grid">
            <div className="stat-card jobs-card">
              <div className="stat-icon">
                <i className="fas fa-briefcase"></i>
              </div>
              <div className="stat-content">
                <div className="stat-number">{stats.totalJobs}</div>
                <div className="stat-label">Total Jobs Posted</div>
                <div className="stat-change positive">
                  <i className="fas fa-arrow-up"></i>
                  +12% from last month
                </div>
              </div>
              <div className="stat-chart">
                <div className="mini-chart jobs-chart"></div>
              </div>
            </div>

            <div className="stat-card applicants-card">
              <div className="stat-icon">
                <i className="fas fa-users"></i>
              </div>
              <div className="stat-content">
                <div className="stat-number">{stats.totalApplicants}</div>
                <div className="stat-label">Total Applicants</div>
                <div className="stat-change positive">
                  <i className="fas fa-arrow-up"></i>
                  +28% from last week
                </div>
              </div>
              <div className="stat-chart">
                <div className="mini-chart applicants-chart"></div>
              </div>
            </div>

            <div className="stat-card match-card">
              <div className="stat-icon">
                <i className="fas fa-bullseye"></i>
              </div>
              <div className="stat-content">
                <div className="stat-number">{stats.topCandidateMatch}%</div>
                <div className="stat-label">Top Candidate Match</div>
                <div className="stat-change positive">
                  <i className="fas fa-arrow-up"></i>
                  +5% accuracy improved
                </div>
              </div>
              <div className="stat-chart">
                <div className="mini-chart match-chart"></div>
              </div>
            </div>

            <div className="stat-card ai-card">
              <div className="stat-icon">
                <i className="fas fa-brain"></i>
              </div>
              <div className="stat-content">
                <div className="stat-number">
                  <span className="status-indicator active"></span>
                  {stats.aiProcessingStatus}
                </div>
                <div className="stat-label">AI Processing Status</div>
                <div className="stat-change neutral">
                  <i className="fas fa-check-circle"></i>
                  All systems operational
                </div>
              </div>
              <div className="stat-chart">
                <div className="mini-chart ai-chart"></div>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="quick-actions-section">
            <h2 className="section-title">
              <i className="fas fa-bolt"></i>
              Quick Actions
            </h2>
            <div className="quick-actions-grid">
              <div className="action-card" onClick={() => navigate('/post-job')}>
                <div className="action-icon">
                  <i className="fas fa-plus-circle"></i>
                </div>
                <h3>Post New Job</h3>
                <p>Create a new job opening and let AI find the best candidates for you</p>
                <button className="action-button">
                  <span>Create Job</span>
                  <i className="fas fa-arrow-right"></i>
                </button>
              </div>

              <div className="action-card" onClick={() => navigate('/candidate-ranking')}>
                <div className="action-icon">
                  <i className="fas fa-chart-bar"></i>
                </div>
                <h3>Candidate Ranking</h3>
                <p>AI-powered candidate ranking and management system</p>
                <div className="action-stats">
                  <span><strong>{stats.totalApplicants}</strong> Candidates</span>
                  <span><strong>0</strong> High Match</span>
                  <span><strong>2</strong> Shortlisted</span>
                </div>
                <button className="action-button">
                  <span>View Rankings</span>
                  <i className="fas fa-arrow-right"></i>
                </button>
              </div>

              <div className="action-card" onClick={() => navigate('/communication')}>
                <div className="action-icon">
                  <i className="fas fa-envelope"></i>
                </div>
                <h3>Communication</h3>
                <p>Send emails and schedule interviews with candidates</p>
                <button className="action-button">
                  <span>Open Communication</span>
                  <i className="fas fa-arrow-right"></i>
                </button>
              </div>

              <div className="action-card" onClick={() => navigate('/employee-management')}>
                <div className="action-icon">
                  <i className="fas fa-users-cog"></i>
                </div>
                <h3>Employee Management</h3>
                <p>Manage employee information, attendance, and performance</p>
                <button className="action-button">
                  <span>Manage Employees</span>
                  <i className="fas fa-arrow-right"></i>
                </button>
              </div>
            </div>
          </div>

          {/* Main Content Grid */}
          <div className="dashboard-content">
            {/* Recent Activities */}
            <div className="content-card activities-card">
              <div className="card-header">
                <h2>
                  <i className="fas fa-clock"></i>
                  Recent Activities
                </h2>
                <button className="view-all-btn">
                  View All
                  <i className="fas fa-arrow-right"></i>
                </button>
              </div>
              <div className="activities-list">
                {recentActivities.length > 0 ? (
                  recentActivities.map(activity => (
                    <div key={activity.id} className="activity-item">
                      <div className={`activity-icon ${activity.type}`}>
                        <i className={getActivityIcon(activity.type)}></i>
                      </div>
                      <div className="activity-content">
                        <p className="activity-text">{activity.action}</p>
                        <div className="activity-meta">
                          <span className="activity-user">{activity.user}</span>
                          <span className="activity-time">{activity.time}</span>
                        </div>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="no-activities">
                    <i className="fas fa-inbox"></i>
                    <p>No recent activities</p>
                  </div>
                )}
              </div>
            </div>

            {/* Top Candidates */}
            <div className="content-card candidates-card">
              <div className="card-header">
                <h2>
                  <i className="fas fa-star"></i>
                  Top Matched Candidates
                </h2>
                <button className="view-all-btn">
                  View All
                  <i className="fas fa-arrow-right"></i>
                </button>
              </div>
              <div className="candidates-list">
                {topCandidates.map(candidate => (
                  <div key={candidate.id} className="candidate-item">
                    <div className="candidate-avatar">
                      {candidate.avatar}
                    </div>
                    <div className="candidate-info">
                      <h4>{candidate.name}</h4>
                      <p>{candidate.position}</p>
                      <div className="candidate-skills">
                        {candidate.skills.slice(0, 3).map(skill => (
                          <span key={skill} className="skill-tag">{skill}</span>
                        ))}
                        {candidate.skills.length > 3 && (
                          <span className="skill-more">+{candidate.skills.length - 3}</span>
                        )}
                      </div>
                    </div>
                    <div className="candidate-match">
                      <div className="match-score">{candidate.match}%</div>
                      <div 
                        className="status-badge"
                        style={{ backgroundColor: getStatusColor(candidate.status) }}
                      >
                        {candidate.status}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* AI Insights */}
            <div className="content-card insights-card">
              <div className="card-header">
                <h2>
                  <i className="fas fa-brain"></i>
                  AI Insights
                </h2>
              </div>
              <div className="insights-grid">
                {aiInsights.map((insight, index) => (
                  <div key={index} className="insight-item">
                    <div className="insight-icon" style={{ color: insight.color }}>
                      <i className={insight.icon}></i>
                    </div>
                    <div className="insight-content">
                      <h4>{insight.title}</h4>
                      {Array.isArray(insight.data) ? (
                        <div className="skill-tags">
                          {insight.data.map(item => (
                            <span key={item} className="insight-tag">{item}</span>
                          ))}
                        </div>
                      ) : (
                        <div className="insight-value">{insight.data}</div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </>
      ) : (
        /* Candidate Dashboard */
        <div className="candidate-dashboard">
          <div className="welcome-card">
            <div className="welcome-content">
              <h2>Welcome to AI HR System</h2>
              <p>Your AI-powered career companion is here to help you find the perfect job match!</p>
              <div className="quick-stats">
                <div className="quick-stat">
                  <i className="fas fa-paper-plane"></i>
                  <span>{stats.totalApplicants} Applications</span>
                </div>
                <div className="quick-stat">
                  <i className="fas fa-bullseye"></i>
                  <span>{stats.topCandidateMatch}% Best Match</span>
                </div>
                <div className="quick-stat">
                  <i className="fas fa-eye"></i>
                  <span>12 Profile Views</span>
                </div>
              </div>
            </div>
            <div className="welcome-actions">
              <button className="action-btn primary" onClick={() => navigate('/upload-resume')}>
                <i className="fas fa-upload"></i>
                Upload Resume
              </button>
              <button className="action-btn secondary" onClick={() => navigate('/browse-jobs')}>
                <i className="fas fa-search"></i>
                Browse Jobs
              </button>
            </div>
          </div>

          <div className="candidate-content">
            <div className="content-card profile-card">
              <div className="card-header">
                <h2>
                  <i className="fas fa-user"></i>
                  Your Profile Status
                </h2>
              </div>
              <div className="profile-progress">
                <div className={`progress-item ${profileStatus.profileCreated ? 'completed' : 'pending'}`}>
                  <i className={`fas ${profileStatus.profileCreated ? 'fa-check-circle' : 'fa-clock'}`}></i>
                  <span>Profile Created</span>
                </div>
                <div className={`progress-item ${profileStatus.resumeUploaded ? 'completed' : 'pending'}`}>
                  <i className={`fas ${profileStatus.resumeUploaded ? 'fa-check-circle' : 'fa-clock'}`}></i>
                  <span>Resume Uploaded</span>
                </div>
                <div className={`progress-item ${profileStatus.skillsVerified ? 'completed' : 'pending'}`}>
                  <i className={`fas ${profileStatus.skillsVerified ? 'fa-check-circle' : 'fa-clock'}`}></i>
                  <span>Skills Verification</span>
                </div>
                <div className={`progress-item ${profileStatus.interviewScheduled ? 'completed' : 'pending'}`}>
                  <i className={`fas ${profileStatus.interviewScheduled ? 'fa-check-circle' : 'fa-clock'}`}></i>
                  <span>Interview Scheduled</span>
                </div>
              </div>
            </div>

            <div className="content-card applications-card">
              <div className="card-header">
                <h2>
                  <i className="fas fa-briefcase"></i>
                  Recent Applications
                </h2>
              </div>
              <div className="applications-list">
                {candidateApplications.length > 0 ? (
                  candidateApplications.map((app) => (
                    <div key={app.id} className="application-item">
                      <div className="app-info">
                        <h4>{app.jobTitle}</h4>
                        <p>{app.company}</p>
                      </div>
                      <div className="app-status">
                        <span 
                          className="status-badge" 
                          style={{ backgroundColor: getStatusColor(app.status) }}
                        >
                          {app.status}
                        </span>
                        <span className="match-score">{app.matchScore}%</span>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="no-applications">
                    <i className="fas fa-inbox"></i>
                    <p>No applications yet</p>
                    <button 
                      className="btn-browse-jobs"
                      onClick={() => navigate('/browse-jobs')}
                    >
                      <i className="fas fa-search"></i>
                      Browse Jobs
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;