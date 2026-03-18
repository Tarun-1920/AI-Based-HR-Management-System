import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './DocumentManagement.css';

const DocumentList = ({ employeeId, refreshTrigger }) => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchDocuments();
  }, [employeeId, refreshTrigger, filter]);

  const fetchDocuments = async () => {
    try {
      const params = {};
      if (employeeId) params.employeeId = employeeId;
      if (filter !== 'all') params.documentType = filter;

      const response = await axios.get('http://localhost:5001/api/documents', { params });
      setDocuments(response.data.documents);
    } catch (error) {
      console.error('Error fetching documents:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (id, originalName) => {
    try {
      const response = await axios.get(`http://localhost:5001/api/documents/${id}/download`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', originalName);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      alert('Download failed');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this document?')) return;

    try {
      await axios.delete(`http://localhost:5001/api/documents/${id}`);
      fetchDocuments();
    } catch (error) {
      alert('Delete failed');
    }
  };

  const formatDate = (date) => new Date(date).toLocaleDateString();
  const formatSize = (bytes) => (bytes / 1024).toFixed(2) + ' KB';

  if (loading) return <div className="loading">Loading documents...</div>;

  return (
    <div className="document-list">
      <div className="list-header">
        <h3>Documents</h3>
        <select value={filter} onChange={(e) => setFilter(e.target.value)} className="filter-select">
          <option value="all">All Types</option>
          <option value="resume">Resume</option>
          <option value="certificate">Certificate</option>
          <option value="offer_letter">Offer Letter</option>
          <option value="employee_report">Employee Report</option>
          <option value="other">Other</option>
        </select>
      </div>

      {documents.length === 0 ? (
        <p className="no-documents">No documents found</p>
      ) : (
        <table className="document-table">
          <thead>
            <tr>
              <th>Document Name</th>
              <th>Type</th>
              <th>Employee ID</th>
              <th>Upload Date</th>
              <th>Size</th>
              <th>Version</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {documents.map((doc) => (
              <tr key={doc._id}>
                <td>{doc.originalName}</td>
                <td><span className="doc-type">{doc.documentType}</span></td>
                <td>{doc.employeeId}</td>
                <td>{formatDate(doc.uploadDate)}</td>
                <td>{formatSize(doc.fileSize)}</td>
                <td>v{doc.version}</td>
                <td className="actions">
                  <button onClick={() => handleDownload(doc._id, doc.originalName)} className="btn-download">
                    Download
                  </button>
                  <button onClick={() => handleDelete(doc._id)} className="btn-delete">
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default DocumentList;
