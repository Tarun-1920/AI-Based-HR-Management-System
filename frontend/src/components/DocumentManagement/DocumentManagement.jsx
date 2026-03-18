import React, { useState } from 'react';
import DocumentUpload from './DocumentUpload';
import DocumentList from './DocumentList';
import './DocumentManagement.css';

const DocumentManagement = () => {
  const [employeeId, setEmployeeId] = useState('');
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleUploadSuccess = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="document-management-container">
      <h2>Document Management System</h2>
      
      <div className="employee-filter">
        <label>Filter by Employee ID:</label>
        <input 
          type="text" 
          value={employeeId} 
          onChange={(e) => setEmployeeId(e.target.value)}
          placeholder="Enter Employee ID (optional)"
        />
      </div>

      <div className="management-grid">
        <DocumentUpload 
          employeeId={employeeId || 'EMP001'} 
          onUploadSuccess={handleUploadSuccess} 
        />
        <DocumentList 
          employeeId={employeeId} 
          refreshTrigger={refreshTrigger} 
        />
      </div>
    </div>
  );
};

export default DocumentManagement;
