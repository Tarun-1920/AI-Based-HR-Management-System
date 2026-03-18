import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import PostJob from './pages/PostJob';
import UploadResume from './pages/UploadResume';
import BrowseJobs from './pages/BrowseJobs';
import CandidateRanking from './pages/CandidateRanking';
import Communication from './pages/Communication';
import EmployeeManagement from './pages/EmployeeManagement';
import Chatbot from './pages/Chatbot';
import './styles/App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userRole, setUserRole] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    const role = localStorage.getItem('userRole');
    
    if (token && role) {
      setIsAuthenticated(true);
      setUserRole(role);
    }
    setIsLoading(false);
  }, []);

  const handleLogin = (role) => {
    setIsAuthenticated(true);
    setUserRole(role);
    localStorage.setItem('userRole', role);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setUserRole('');
    localStorage.removeItem('authToken');
    localStorage.removeItem('userRole');
    localStorage.removeItem('userName');
  };

  if (isLoading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <div>Loading...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <Router>
        <Routes>
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
          <Route path="/register" element={<Register />} />
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </Router>
    );
  }

  return (
    <Router>
      <div className="app">
        <Sidebar userRole={userRole} onLogout={handleLogout} />
        <div className="main-content">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" />} />
            <Route path="/dashboard" element={<Dashboard userRole={userRole} />} />
            <Route path="/post-job" element={<PostJob />} />
            <Route path="/upload-resume" element={<UploadResume />} />
            <Route path="/browse-jobs" element={<BrowseJobs />} />
            <Route path="/candidates" element={<CandidateRanking />} />
            <Route path="/communication" element={<Communication />} />
            <Route path="/employees" element={<EmployeeManagement />} />
            <Route path="/chatbot" element={<Chatbot />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;