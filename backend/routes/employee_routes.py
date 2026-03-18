from flask import Blueprint, request, jsonify
from models.employee_model import Employee
from models.attendance_model import Attendance
from models.leave_model import Leave
from datetime import datetime
from bson import ObjectId

employee_bp = Blueprint('employees', __name__)

# Employee CRUD Operations
@employee_bp.route('/', methods=['POST'])
def create_employee():
    try:
        data = request.get_json()
        
        required_fields = ['employee_id', 'name', 'email', 'phone', 'department', 'role', 'joining_date', 'salary']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        if Employee.find_by_employee_id(data['employee_id']):
            return jsonify({'error': 'Employee ID already exists'}), 400
        
        if Employee.find_by_email(data['email']):
            return jsonify({'error': 'Email already exists'}), 400
        
        employee_id = Employee.create(
            employee_id=data['employee_id'],
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            address=data.get('address', ''),
            department=data['department'],
            role=data['role'],
            joining_date=data['joining_date'],
            experience=data.get('experience', ''),
            skills=data.get('skills', []),
            salary=data['salary']
        )
        
        return jsonify({
            'success': True,
            'message': 'Employee created successfully',
            'employee_id': employee_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/', methods=['GET'])
def get_all_employees():
    try:
        employees = Employee.find_all()
        
        result = []
        for emp in employees:
            result.append({
                'id': str(emp['_id']),
                'employee_id': emp.get('employee_id'),
                'name': emp.get('name'),
                'email': emp.get('email'),
                'phone': emp.get('phone'),
                'department': emp.get('department'),
                'role': emp.get('role'),
                'status': emp.get('status'),
                'joining_date': emp.get('joining_date')
            })
        
        return jsonify({
            'success': True,
            'count': len(result),
            'employees': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/<employee_id>', methods=['GET'])
def get_employee(employee_id):
    try:
        employee = Employee.find_by_id(employee_id)
        
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        employee['_id'] = str(employee['_id'])
        
        return jsonify({
            'success': True,
            'employee': employee
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/<employee_id>', methods=['PUT'])
def update_employee(employee_id):
    try:
        data = request.get_json()
        
        employee = Employee.find_by_id(employee_id)
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        Employee.update(employee_id, data)
        
        return jsonify({
            'success': True,
            'message': 'Employee updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/<employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    try:
        employee = Employee.find_by_id(employee_id)
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        Employee.delete(employee_id)
        
        return jsonify({
            'success': True,
            'message': 'Employee deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Attendance APIs
@employee_bp.route('/<employee_id>/attendance', methods=['POST'])
def mark_attendance(employee_id):
    try:
        data = request.get_json()
        
        date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
        status = data.get('status', 'present')
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        
        existing = Attendance.find_by_date(employee_id, date)
        if existing:
            return jsonify({'error': 'Attendance already marked for this date'}), 400
        
        attendance_id = Attendance.mark_attendance(employee_id, date, status, check_in, check_out)
        
        return jsonify({
            'success': True,
            'message': 'Attendance marked successfully',
            'attendance_id': attendance_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/<employee_id>/attendance', methods=['GET'])
def get_attendance(employee_id):
    try:
        month = request.args.get('month', type=int)
        year = request.args.get('year', type=int)
        
        attendance = Attendance.find_by_employee(employee_id, month, year)
        
        result = []
        for att in attendance:
            result.append({
                'id': str(att['_id']),
                'date': att.get('date'),
                'status': att.get('status'),
                'check_in': att.get('check_in'),
                'check_out': att.get('check_out')
            })
        
        return jsonify({
            'success': True,
            'count': len(result),
            'attendance': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Leave APIs
@employee_bp.route('/<employee_id>/leave', methods=['POST'])
def apply_leave(employee_id):
    try:
        data = request.get_json()
        
        required_fields = ['leave_type', 'start_date', 'end_date', 'reason', 'days']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        leave_id = Leave.create(
            employee_id=employee_id,
            leave_type=data['leave_type'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            reason=data['reason'],
            days=data['days']
        )
        
        return jsonify({
            'success': True,
            'message': 'Leave applied successfully',
            'leave_id': leave_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/<employee_id>/leave', methods=['GET'])
def get_leaves(employee_id):
    try:
        leaves = Leave.find_by_employee(employee_id)
        
        result = []
        for leave in leaves:
            result.append({
                'id': str(leave['_id']),
                'leave_type': leave.get('leave_type'),
                'start_date': leave.get('start_date'),
                'end_date': leave.get('end_date'),
                'reason': leave.get('reason'),
                'days': leave.get('days'),
                'status': leave.get('status'),
                'created_at': leave.get('created_at').isoformat() if leave.get('created_at') else None
            })
        
        return jsonify({
            'success': True,
            'count': len(result),
            'leaves': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/leave/<leave_id>/approve', methods=['PUT'])
def approve_leave(leave_id):
    try:
        data = request.get_json()
        approved_by = data.get('approved_by', 'HR Manager')
        
        leave = Leave.find_by_id(leave_id)
        if not leave:
            return jsonify({'error': 'Leave not found'}), 404
        
        Leave.approve(leave_id, approved_by)
        
        return jsonify({
            'success': True,
            'message': 'Leave approved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/leave/<leave_id>/reject', methods=['PUT'])
def reject_leave(leave_id):
    try:
        data = request.get_json()
        approved_by = data.get('approved_by', 'HR Manager')
        
        leave = Leave.find_by_id(leave_id)
        if not leave:
            return jsonify({'error': 'Leave not found'}), 404
        
        Leave.reject(leave_id, approved_by)
        
        return jsonify({
            'success': True,
            'message': 'Leave rejected successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Performance APIs
@employee_bp.route('/<employee_id>/performance', methods=['PUT'])
def update_performance(employee_id):
    try:
        data = request.get_json()
        
        employee = Employee.find_by_id(employee_id)
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        performance = {
            'performance.rating': data.get('rating', 0),
            'performance.feedback': data.get('feedback', ''),
            'performance.score': data.get('score', 0)
        }
        
        Employee.update(employee_id, performance)
        
        return jsonify({
            'success': True,
            'message': 'Performance updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
