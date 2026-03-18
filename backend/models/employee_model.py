from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from database import get_collection

employees_collection = get_collection('employees')

class Employee:
    @staticmethod
    def create(employee_id, name, email, phone, address, department, role, joining_date, experience, skills, salary):
        employee = {
            'employee_id': employee_id,
            'name': name,
            'email': email,
            'phone': phone,
            'address': address,
            'department': department,
            'role': role,
            'joining_date': joining_date,
            'experience': experience,
            'skills': skills,
            'salary': salary,
            'status': 'active',
            'performance': {
                'rating': 0,
                'feedback': '',
                'score': 0
            },
            'documents': [],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = employees_collection.insert_one(employee)
        return str(result.inserted_id)

    @staticmethod
    def find_all():
        return list(employees_collection.find())

    @staticmethod
    def find_by_id(employee_id):
        try:
            return employees_collection.find_one({'_id': ObjectId(employee_id)})
        except:
            return None

    @staticmethod
    def find_by_employee_id(employee_id):
        return employees_collection.find_one({'employee_id': employee_id})

    @staticmethod
    def find_by_email(email):
        return employees_collection.find_one({'email': email})

    @staticmethod
    def update(employee_id, data):
        data['updated_at'] = datetime.utcnow()
        return employees_collection.update_one({'_id': ObjectId(employee_id)}, {'$set': data})

    @staticmethod
    def delete(employee_id):
        return employees_collection.delete_one({'_id': ObjectId(employee_id)})

    @staticmethod
    def find_by_department(department):
        return list(employees_collection.find({'department': department}))
