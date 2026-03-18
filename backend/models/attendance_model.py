from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from database import get_collection

attendance_collection = get_collection('attendance')

class Attendance:
    @staticmethod
    def mark_attendance(employee_id, date, status, check_in=None, check_out=None):
        attendance = {
            'employee_id': employee_id,
            'date': date,
            'status': status,
            'check_in': check_in,
            'check_out': check_out,
            'created_at': datetime.utcnow()
        }
        result = attendance_collection.insert_one(attendance)
        return str(result.inserted_id)

    @staticmethod
    def find_by_employee(employee_id, month=None, year=None):
        query = {'employee_id': employee_id}
        if month and year:
            query['date'] = {
                '$regex': f'^{year}-{month:02d}'
            }
        return list(attendance_collection.find(query).sort('date', -1))

    @staticmethod
    def find_by_date(employee_id, date):
        return attendance_collection.find_one({'employee_id': employee_id, 'date': date})

    @staticmethod
    def update(attendance_id, data):
        return attendance_collection.update_one({'_id': ObjectId(attendance_id)}, {'$set': data})
