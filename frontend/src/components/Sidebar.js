import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../styles/Sidebar.css';

const Sidebar = ({ userRole, onLogout }) => {
  const location = useLocation();
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [showLogoutConfirm, setShowLogoutConfirm] = useState(false);

  // Menu items based on user role
  const getMenuItems = () => {
    const commonItems = [
      {
        path: '/dashboard',
        icon: 'fas fa-tachometer-alt',
        label: 'Dashboard',
        roles: ['hr', 'candidate']
      },
      {
        path: '/chatbot',
        icon: 'fas fa-robot',
        label: userRole === 'candidate' ? 'Career Assistant' : 'HR Assistant',
        roles: ['hr', 'candidate']
      }
    ];

    const hrItems = [
      {
        path: '/post-job',
        icon: 'fas fa-plus-circle',
        label: 'Post Job',
        roles: ['hr']
      },
      {
        path: '/candidates',
        icon: 'fas fa-users',
        label: 'Candidates',
        roles: ['hr']
      },
      {
        path: '/communication',
        icon: 'fas fa-envelope',
        label: 'Communication',
        roles: ['hr']
      },
      {
        path: '/employees',
        icon: 'fas fa-users-cog',
        label: 'Employees',
        roles: ['hr']
      }
    ];

    const candidateItems = [
      {
        path: '/browse-jobs',
        icon: 'fas fa-search',
        label: 'Browse Jobs',
        roles: ['candidate']
      },
      {
        path: '/upload-resume',
        icon: 'fas fa-upload',
        label: 'Upload Resume',
        roles: ['candidate']
      }
    ];

    const allItems = [...commonItems];
    
    if (userRole === 'hr') {
      allItems.push(...hrItems);
    } else if (userRole === 'candidate') {
      allItems.push(...candidateItems);
    }

    return allItems;
  };

  const menuItems = getMenuItems();

  const isActive = (path) => {
    return location.pathname === path;
  };

  const handleLogout = () => {
    setShowLogoutConfirm(false);
    onLogout();
  };

  const getUserInitials = () => {
    if (userRole === 'hr') {
      return 'HR';
    } else if (userRole === 'candidate') {
      return 'CD';
    }
    return 'US';
  };

  const getUserName = () => {
    if (userRole === 'hr') {
      return 'HR Manager';
    } else if (userRole === 'candidate') {
      return 'Candidate';
    }
    return 'User';
  };

  return (
    <>
      {/* Sidebar */}
      <div className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}>
        {/* Logo Section */}
        <div className="sidebar-logo">
          <div className="logo-icon">
            <i className="fas fa-brain"></i>
          </div>
          {!isCollapsed && (
            <div className="logo-text">
              <h2>AI HR</h2>
              <p>System</p>
            </div>
          )}
        </div>

        {/* Collapse Toggle */}
        <button 
          className="collapse-btn"
          onClick={() => setIsCollapsed(!isCollapsed)}
          title={isCollapsed ? 'Expand' : 'Collapse'}
        >
          <i className={`fas fa-chevron-${isCollapsed ? 'right' : 'left'}`}></i>
        </button>

        {/* Navigation Menu */}
        <nav className="sidebar-nav">
          <div className="nav-section">
            {menuItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`nav-item ${isActive(item.path) ? 'active' : ''}`}
                title={isCollapsed ? item.label : ''}
              >
                <div className="nav-icon">
                  <i className={item.icon}></i>
                </div>
                {!isCollapsed && (
                  <>
                    <span className="nav-label">{item.label}</span>
                    {isActive(item.path) && (
                      <div className="active-indicator"></div>
                    )}
                  </>
                )}
              </Link>
            ))}
          </div>
        </nav>

        {/* Sidebar Footer */}
        <div className="sidebar-footer">
          {/* User Info */}
          <div className="user-section">
            <div className="user-avatar">
              {getUserInitials()}
            </div>
            {!isCollapsed && (
              <div className="user-info">
                <p className="user-name">{getUserName()}</p>
                <p className="user-role">{userRole === 'hr' ? 'HR Manager' : 'Candidate'}</p>
              </div>
            )}
          </div>

          {/* Logout Button */}
          <button
            className="logout-btn"
            onClick={() => setShowLogoutConfirm(true)}
            title="Logout"
          >
            <i className="fas fa-sign-out-alt"></i>
            {!isCollapsed && <span>Logout</span>}
          </button>
        </div>
      </div>

      {/* Logout Confirmation Modal */}
      {showLogoutConfirm && (
        <div className="logout-modal-overlay">
          <div className="logout-modal">
            <div className="modal-header">
              <i className="fas fa-exclamation-circle"></i>
              <h3>Confirm Logout</h3>
            </div>
            <p className="modal-message">
              Are you sure you want to logout? You will need to login again to access the system.
            </p>
            <div className="modal-actions">
              <button
                className="btn-cancel"
                onClick={() => setShowLogoutConfirm(false)}
              >
                <i className="fas fa-times"></i>
                Cancel
              </button>
              <button
                className="btn-confirm"
                onClick={handleLogout}
              >
                <i className="fas fa-check"></i>
                Logout
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Sidebar;
