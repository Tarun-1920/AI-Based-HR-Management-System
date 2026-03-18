from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from database import get_collection

leaves_collection = get_collection('leaves')

class Leave:
    @staticmethod
    def create(employee_id, leave_type, start_date, end_date, reason, days):
        leave = {
            'employee_id': employee_id,
            'leave_type': leave_type,
            'start_date': start_date,
            'end_date': end_date,
            'reason': reason,
            'days': days,
            'status': 'pending',
            'approved_by': None,
            'approved_at': None,
            'created_at': datetime.utcnow()
        }
        result = leaves_collection.insert_one(leave)
        return str(result.inserted_id)

    @staticmethod
    def find_all():
        return list(leaves_collection.find().sort('created_at', -1))

    @staticmethod
    def find_by_employee(employee_id):
        return list(leaves_collection.find({'employee_id': employee_id}).sort('created_at', -1))

    @staticmethod
    def find_by_id(leave_id):
        try:
            return leaves_collection.find_one({'_id': ObjectId(leave_id)})
        except:
            return None

    @staticmethod
    def update(leave_id, data):
        return leaves_collection.update_one({'_id': ObjectId(leave_id)}, {'$set': data})

    @staticmethod
    def approve(leave_id, approved_by):
        return leaves_collection.update_one(
            {'_id': ObjectId(leave_id)},
            {'$set': {
                'status': 'approved',
                'approved_by': approved_by,
                'approved_at': datetime.utcnow()
            }}
        )

    @staticmethod
    def reject(leave_id, approved_by):
        return leaves_collection.update_one(
            {'_id': ObjectId(leave_id)},
            {'$set': {
                'status': 'rejected',
                'approved_by': approved_by,
                'approved_at': datetime.utcnow()
            }}
        )
