from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from database import get_collection

jobs_collection = get_collection('jobs')

class Job:
    @staticmethod
    def create(title, description, requirements, location, experience, salary_range=''):
        job = {
            'job_title': title,
            'description': description,
            'required_skills': requirements,
            'experience': experience,
            'location': location,
            'salary_range': salary_range,
            'status': 'open',
            'created_at': datetime.utcnow()
        }
        result = jobs_collection.insert_one(job)
        return str(result.inserted_id)

    @staticmethod
    def find_all():
        return list(jobs_collection.find())

    @staticmethod
    def find_by_id(job_id):
        try:
            return jobs_collection.find_one({'_id': ObjectId(job_id)})
        except:
            return None

    @staticmethod
    def update(job_id, data):
        return jobs_collection.update_one({'_id': ObjectId(job_id)}, {'$set': data})

    @staticmethod
    def delete(job_id):
        return jobs_collection.delete_one({'_id': ObjectId(job_id)})
