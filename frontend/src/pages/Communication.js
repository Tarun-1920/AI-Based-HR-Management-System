import React, { useState, useEffect } from 'react';
import { candidatesAPI } from '../utils/api';
import axios from 'axios';
import '../styles/Communication.css';

const API_BASE_URL = 'http://localhost:5000/api';

const Communication = () => {
  const [candidates, setCandidates] = useState([]);
  const [selectedCandidate, setSelectedCandidate] = useState('');
  const [templateType, setTemplateType] = useState('');
  const [customData, setCustomData] = useState({});
  const [communicationHistory, setCommunicationHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  const [activeTab, setActiveTab] = useState('send');

  const templates = [
    { value: 'application_received', label: 'Application Received' },
    { value: 'interview_invitation', label: 'Interview Invitation' },
    { value: 'interview_feedback', label: 'Interview Feedback' },
    { value: 'rejection', label: 'Rejection Email' },
    { value: 'offer_letter', label: 'Offer Letter' },
    { value: 'interview_reminder', label: 'Interview Reminder' }
  ];

  useEffect(() => {
    fetchCandidates();
  }, []);

  const fetchCandidates = async () => {
    try {
      const response = await candidatesAPI.getAllCandidates();
      setCandidates(response.candidates || []);
    } catch (error) {
      console.error('Error fetching candidates:', error);
    }
  };

  const fetchCommunicationHistory = async (candidateId) => {
    try {
      const token = localStorage.getItem('authToken');
      const response = await axios.get(
        `${API_BASE_URL}/communications/history/${candidateId}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setCommunicationHistory(response.data.communications || []);
    } catch (error) {
      console.error('Error fetching history:', error);
    }
  };

  const handleCandidateChange = (e) => {
    const candidateId = e.target.value;
    setSelectedCandidate(candidateId);
    if (candidateId) {
      fetchCommunicationHistory(candidateId);
    }
  };

  const handleSendCommunication = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage({ type: '', text: '' });

    try {
      const token = localStorage.getItem('authToken');
      await axios.post(
        `${API_BASE_URL}/communications/send`,
        {
          candidate_id: selectedCandidate,
          template_type: templateType,
          custom_data: customData
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setMessage({ type: 'success', text: 'Communication sent successfully!' });
      setTemplateType('');
      setCustomData({});
      fetchCommunicationHistory(selectedCandidate);
    } catch (error) {
      setMessage({ type: 'error', text: error.response?.data?.error || 'Failed to send communication' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleScheduleInterview = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage({ type: '', text: '' });

    try {
      const token = localStorage.getItem('authToken');
      await axios.post(
        `${API_BASE_URL}/communications/schedule-interview`,
        {
          candidate_id: selectedCandidate,
          interview_date: customData.interview_date,
          interview_time: customData.interview_time,
          interview_location: customData.interview_location,
          interviewer_name: customData.interviewer_name
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setMessage({ type: 'success', text: 'Interview scheduled successfully!' });
      setCustomData({});
      fetchCommunicationHistory(selectedCandidate);
    } catch (error) {
      setMessage({ type: 'error', text: error.response?.data?.error || 'Failed to schedule interview' });
    } finally {
      setIsLoading(false);
    }
  };

  const renderCustomFields = () => {
    if (templateType === 'interview_invitation') {
      return (
        <>
          <div className="form-group">
            <label>Interview Date</label>
            <input
              type="date"
              value={customData.interview_date || ''}
              onChange={(e) => setCustomData({ ...customData, interview_date: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Interview Time</label>
            <input
              type="time"
              value={customData.interview_time || ''}
              onChange={(e) => setCustomData({ ...customData, interview_time: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Interview Location</label>
            <input
              type="text"
              value={customData.interview_location || ''}
              onChange={(e) => setCustomData({ ...customData, interview_location: e.target.value })}
              placeholder="e.g., Office Room 301 or Zoom Link"
              required
            />
          </div>
          <div className="form-group">
            <label>Interviewer Name</label>
            <input
              type="text"
              value={customData.interviewer_name || ''}
              onChange={(e) => setCustomData({ ...customData, interviewer_name: e.target.value })}
              placeholder="e.g., John Doe"
            />
          </div>
        </>
      );
    }

    if (templateType === 'interview_feedback') {
      return (
        <div className="form-group">
          <label>Feedback Message</label>
          <textarea
            value={customData.feedback_message || ''}
            onChange={(e) => setCustomData({ ...customData, feedback_message: e.target.value })}
            rows="4"
            placeholder="Enter your feedback..."
            required
          />
        </div>
      );
    }

    if (templateType === 'offer_letter') {
      return (
        <>
          <div className="form-group">
            <label>Start Date</label>
            <input
              type="date"
              value={customData.start_date || ''}
              onChange={(e) => setCustomData({ ...customData, start_date: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Salary</label>
            <input
              type="text"
              value={customData.salary || ''}
              onChange={(e) => setCustomData({ ...customData, salary: e.target.value })}
              placeholder="e.g., $80,000 - $100,000"
              required
            />
          </div>
          <div className="form-group">
            <label>Location</label>
            <input
              type="text"
              value={customData.location || ''}
              onChange={(e) => setCustomData({ ...customData, location: e.target.value })}
              placeholder="e.g., New York, NY"
              required
            />
          </div>
        </>
      );
    }

    return null;
  };

  return (
    <div className="communication-container">
      <div className="page-header">
        <h1>
          <i className="fas fa-envelope"></i>
          Candidate Communication
        </h1>
        <p>Send emails and schedule interviews with candidates</p>
      </div>

      {message.text && (
        <div className={`message ${message.type}`}>
          <i className={`fas fa-${message.type === 'success' ? 'check-circle' : 'exclamation-circle'}`}></i>
          {message.text}
        </div>
      )}

      <div className="communication-content">
        <div className="left-panel">
          <div className="tabs">
            <button
              className={`tab ${activeTab === 'send' ? 'active' : ''}`}
              onClick={() => setActiveTab('send')}
            >
              <i className="fas fa-paper-plane"></i>
              Send Email
            </button>
            <button
              className={`tab ${activeTab === 'schedule' ? 'active' : ''}`}
              onClick={() => setActiveTab('schedule')}
            >
              <i className="fas fa-calendar-alt"></i>
              Schedule Interview
            </button>
          </div>

          <div className="form-section">
            <div className="form-group">
              <label>Select Candidate *</label>
              <select value={selectedCandidate} onChange={handleCandidateChange} required>
                <option value="">-- Select Candidate --</option>
                {candidates.map(candidate => (
                  <option key={candidate.candidate_id} value={candidate.candidate_id}>
                    {candidate.candidate_name} - {candidate.email}
                  </option>
                ))}
              </select>
            </div>

            {activeTab === 'send' && (
              <form onSubmit={handleSendCommunication}>
                <div className="form-group">
                  <label>Email Template *</label>
                  <select value={templateType} onChange={(e) => setTemplateType(e.target.value)} required>
                    <option value="">-- Select Template --</option>
                    {templates.map(template => (
                      <option key={template.value} value={template.value}>
                        {template.label}
                      </option>
                    ))}
                  </select>
                </div>

                {renderCustomFields()}

                <button type="submit" className="btn-primary" disabled={isLoading || !selectedCandidate}>
                  {isLoading ? (
                    <>
                      <i className="fas fa-spinner fa-spin"></i>
                      Sending...
                    </>
                  ) : (
                    <>
                      <i className="fas fa-paper-plane"></i>
                      Send Email
                    </>
                  )}
                </button>
              </form>
            )}

            {activeTab === 'schedule' && (
              <form onSubmit={handleScheduleInterview}>
                <div className="form-group">
                  <label>Interview Date *</label>
                  <input
                    type="date"
                    value={customData.interview_date || ''}
                    onChange={(e) => setCustomData({ ...customData, interview_date: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Interview Time *</label>
                  <input
                    type="time"
                    value={customData.interview_time || ''}
                    onChange={(e) => setCustomData({ ...customData, interview_time: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Interview Location *</label>
                  <input
                    type="text"
                    value={customData.interview_location || ''}
                    onChange={(e) => setCustomData({ ...customData, interview_location: e.target.value })}
                    placeholder="e.g., Office Room 301 or Zoom Link"
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Interviewer Name</label>
                  <input
                    type="text"
                    value={customData.interviewer_name || ''}
                    onChange={(e) => setCustomData({ ...customData, interviewer_name: e.target.value })}
                    placeholder="e.g., John Doe"
                  />
                </div>

                <button type="submit" className="btn-primary" disabled={isLoading || !selectedCandidate}>
                  {isLoading ? (
                    <>
                      <i className="fas fa-spinner fa-spin"></i>
                      Scheduling...
                    </>
                  ) : (
                    <>
                      <i className="fas fa-calendar-check"></i>
                      Schedule Interview
                    </>
                  )}
                </button>
              </form>
            )}
          </div>
        </div>

        <div className="right-panel">
          <div className="history-header">
            <h2>
              <i className="fas fa-history"></i>
              Communication History
            </h2>
          </div>

          {selectedCandidate ? (
            <div className="history-list">
              {communicationHistory.length > 0 ? (
                communicationHistory.map(comm => (
                  <div key={comm.id} className="history-item">
                    <div className="history-icon">
                      <i className="fas fa-envelope"></i>
                    </div>
                    <div className="history-content">
                      <h4>{comm.subject}</h4>
                      <p className="template-type">{comm.template_type.replace('_', ' ').toUpperCase()}</p>
                      <p className="message-preview">{comm.message.substring(0, 100)}...</p>
                      <div className="history-meta">
                        <span>
                          <i className="fas fa-clock"></i>
                          {new Date(comm.sent_at).toLocaleString()}
                        </span>
                        {comm.scheduled_date && (
                          <span>
                            <i className="fas fa-calendar"></i>
                            {comm.scheduled_date}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="no-history">
                  <i className="fas fa-inbox"></i>
                  <p>No communication history found</p>
                </div>
              )}
            </div>
          ) : (
            <div className="no-selection">
              <i className="fas fa-user-circle"></i>
              <p>Select a candidate to view communication history</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Communication;
