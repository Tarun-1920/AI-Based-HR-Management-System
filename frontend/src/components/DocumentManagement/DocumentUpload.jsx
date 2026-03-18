import React, { useState } from 'react';
import axios from 'axios';
import './DocumentManagement.css';

const DocumentUpload = ({ employeeId, onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [documentType, setDocumentType] = useState('resume');
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage('');
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setMessage('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('document', file);
    formData.append('employeeId', employeeId);
    formData.append('documentType', documentType);
    formData.append('uploadedBy', 'HR Admin'); // Replace with actual user

    setUploading(true);
    setMessage('');

    try {
      const response = await axios.post('http://localhost:5001/api/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      setMessage('Document uploaded successfully!');
      setFile(null);
      e.target.reset();
      
      if (onUploadSuccess) onUploadSuccess(response.data.document);
    } catch (error) {
      setMessage(error.response?.data?.error || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="document-upload">
      <h3>Upload Document</h3>
      <form onSubmit={handleUpload}>
        <div className="form-group">
          <label>Document Type:</label>
          <select value={documentType} onChange={(e) => setDocumentType(e.target.value)}>
            <option value="resume">Resume</option>
            <option value="certificate">Certificate</option>
            <option value="offer_letter">Offer Letter</option>
            <option value="employee_report">Employee Report</option>
            <option value="other">Other</option>
          </select>
        </div>
        
        <div className="form-group">
          <label>Select File:</label>
          <input type="file" onChange={handleFileChange} accept=".pdf,.doc,.docx,.jpg,.jpeg,.png,.txt,.xlsx,.xls" />
          {file && <span className="file-name">{file.name}</span>}
        </div>

        <button type="submit" disabled={uploading || !file}>
          {uploading ? 'Uploading...' : 'Upload Document'}
        </button>
      </form>
      
      {message && <div className={`message ${message.includes('success') ? 'success' : 'error'}`}>{message}</div>}
    </div>
  );
};

export default DocumentUpload;
