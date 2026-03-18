import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/EmployeeManagement.css';

const API_BASE_URL = 'http://localhost:5000/api';

const EmployeeManagement = () => {
  const [employees, setEmployees] = useState([]);
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [activeTab, setActiveTab] = useState('list');
  const [formData, setFormData] = useState({
    employee_id: '',
    name: '',
    email: '',
    phone: '',
    address: '',
    department: '',
    role: '',
    joining_date: '',
    experience: '',
    skills: [],
    salary: ''
  });
  const [message, setMessage] = useState({ type: '', text: '' });
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    fetchEmployees();
  }, []);

  const fetchEmployees = async () => {
    try {
      const token = localStorage.getItem('authToken');
      const response = await axios.get(`${API_BASE_URL}/employees`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setEmployees(response.data.employees || []);
    } catch (error) {
      console.error('Error fetching employees:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage({ type: '', text: '' });

    try {
      const token = localStorage.getItem('authToken');
      await axios.post(`${API_BASE_URL}/employees`, formData, {
        headers: { Authorization: `Bearer ${token}` }
      });

      setMessage({ type: 'success', text: 'Employee added successfully!' });
      setFormData({
        employee_id: '',
        name: '',
        email: '',
        phone: '',
        address: '',
        department: '',
        role: '',
        joining_date: '',
        experience: '',
        skills: [],
        salary: ''
      });
      fetchEmployees();
      setActiveTab('list');
    } catch (error) {
      setMessage({ type: 'error', text: error.response?.data?.error || 'Failed to add employee' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (employeeId) => {
    if (!window.confirm('Are you sure you want to delete this employee?')) return;

    try {
      const token = localStorage.getItem('authToken');
      await axios.delete(`${API_BASE_URL}/employees/${employeeId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMessage({ type: 'success', text: 'Employee deleted successfully!' });
      fetchEmployees();
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to delete employee' });
    }
  };

  const viewEmployee = async (employeeId) => {
    try {
      const token = localStorage.getItem('authToken');
      const response = await axios.get(`${API_BASE_URL}/employees/${employeeId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSelectedEmployee(response.data.employee);
      setActiveTab('view');
    } catch (error) {
      console.error('Error fetching employee details:', error);
    }
  };

  return (
    <div className="employee-management-container">
      <div className="page-header">
        <h1>
          <i className="fas fa-users-cog"></i>
          Employee Management
        </h1>
        <p>Manage employee information, attendance, and performance</p>
      </div>

      {message.text && (
        <div className={`message ${message.type}`}>
          <i className={`fas fa-${message.type === 'success' ? 'check-circle' : 'exclamation-circle'}`}></i>
          {message.text}
        </div>
      )}

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'list' ? 'active' : ''}`}
          onClick={() => setActiveTab('list')}
        >
          <i className="fas fa-list"></i>
          Employee List
        </button>
        <button
          className={`tab ${activeTab === 'add' ? 'active' : ''}`}
          onClick={() => setActiveTab('add')}
        >
          <i className="fas fa-user-plus"></i>
          Add Employee
        </button>
      </div>

      {activeTab === 'list' && (
        <div className="employee-list">
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Employee ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Department</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {employees.map(emp => (
                  <tr key={emp.id}>
                    <td>{emp.employee_id}</td>
                    <td>{emp.name}</td>
                    <td>{emp.email}</td>
                    <td>{emp.department}</td>
                    <td>{emp.role}</td>
                    <td>
                      <span className={`status-badge ${emp.status}`}>
                        {emp.status}
                      </span>
                    </td>
                    <td>
                      <button
                        className="btn-view"
                        onClick={() => viewEmployee(emp.id)}
                      >
                        <i className="fas fa-eye"></i>
                      </button>
                      <button
                        className="btn-delete"
                        onClick={() => handleDelete(emp.id)}
                      >
                        <i className="fas fa-trash"></i>
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'add' && (
        <div className="add-employee-form">
          <form onSubmit={handleSubmit}>
            <div className="form-section">
              <h3>Personal Information</h3>
              <div className="form-row">
                <div className="form-group">
                  <label>Employee ID *</label>
                  <input
                    type="text"
                    value={formData.employee_id}
                    onChange={(e) => setFormData({ ...formData, employee_id: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Full Name *</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Email *</label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Phone *</label>
                  <input
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Address</label>
                <textarea
                  value={formData.address}
                  onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                  rows="3"
                />
              </div>
            </div>

            <div className="form-section">
              <h3>Professional Information</h3>
              <div className="form-row">
                <div className="form-group">
                  <label>Department *</label>
                  <select
                    value={formData.department}
                    onChange={(e) => setFormData({ ...formData, department: e.target.value })}
                    required
                  >
                    <option value="">Select Department</option>
                    <option value="Engineering">Engineering</option>
                    <option value="HR">HR</option>
                    <option value="Sales">Sales</option>
                    <option value="Marketing">Marketing</option>
                    <option value="Finance">Finance</option>
                  </select>
                </div>
                <div className="form-group">
                  <label>Role *</label>
                  <input
                    type="text"
                    value={formData.role}
                    onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Joining Date *</label>
                  <input
                    type="date"
                    value={formData.joining_date}
                    onChange={(e) => setFormData({ ...formData, joining_date: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Experience</label>
                  <input
                    type="text"
                    value={formData.experience}
                    onChange={(e) => setFormData({ ...formData, experience: e.target.value })}
                    placeholder="e.g., 3 years"
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Salary *</label>
                <input
                  type="number"
                  value={formData.salary}
                  onChange={(e) => setFormData({ ...formData, salary: e.target.value })}
                  required
                />
              </div>
            </div>

            <button type="submit" className="btn-submit" disabled={isLoading}>
              {isLoading ? (
                <>
                  <i className="fas fa-spinner fa-spin"></i>
                  Adding...
                </>
              ) : (
                <>
                  <i className="fas fa-plus"></i>
                  Add Employee
                </>
              )}
            </button>
          </form>
        </div>
      )}

      {activeTab === 'view' && selectedEmployee && (
        <div className="employee-details">
          <div className="details-header">
            <h2>{selectedEmployee.name}</h2>
            <button className="btn-back" onClick={() => setActiveTab('list')}>
              <i className="fas fa-arrow-left"></i>
              Back to List
            </button>
          </div>

          <div className="details-grid">
            <div className="detail-card">
              <h3>Personal Information</h3>
              <div className="detail-item">
                <span className="label">Employee ID:</span>
                <span className="value">{selectedEmployee.employee_id}</span>
              </div>
              <div className="detail-item">
                <span className="label">Email:</span>
                <span className="value">{selectedEmployee.email}</span>
              </div>
              <div className="detail-item">
                <span className="label">Phone:</span>
                <span className="value">{selectedEmployee.phone}</span>
              </div>
              <div className="detail-item">
                <span className="label">Address:</span>
                <span className="value">{selectedEmployee.address}</span>
              </div>
            </div>

            <div className="detail-card">
              <h3>Professional Information</h3>
              <div className="detail-item">
                <span className="label">Department:</span>
                <span className="value">{selectedEmployee.department}</span>
              </div>
              <div className="detail-item">
                <span className="label">Role:</span>
                <span className="value">{selectedEmployee.role}</span>
              </div>
              <div className="detail-item">
                <span className="label">Joining Date:</span>
                <span className="value">{selectedEmployee.joining_date}</span>
              </div>
              <div className="detail-item">
                <span className="label">Experience:</span>
                <span className="value">{selectedEmployee.experience}</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default EmployeeManagement;
