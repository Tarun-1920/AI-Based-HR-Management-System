import React from 'react';
import DocumentManagement from '../components/DocumentManagement/DocumentManagement';

/**
 * Example HR Documents Page
 * Shows how to integrate the Document Management Module
 */
const HRDocumentsPage = () => {
  return (
    <div className="hr-documents-page">
      <div className="page-header">
        <h1>Employee Documents</h1>
        <p>Manage all employee documents including resumes, certificates, and reports</p>
      </div>
      
      <DocumentManagement />
    </div>
  );
};

export default HRDocumentsPage;

// Add this to your App.js or routing configuration:
/*
import HRDocumentsPage from './pages/HRDocumentsPage';

// In your routes:
<Route path="/hr/documents" element={<HRDocumentsPage />} />
*/
