from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from database import get_collection

candidates_collection = get_collection('candidates')

class Candidate:
    @staticmethod
    def create(name, email, phone, resume_text, skills, experience, job_id):
        candidate = {
            'name': name,
            'email': email,
            'phone': phone,
            'resume_text': resume_text,
            'skills': skills,
            'experience': experience,
            'job_id': job_id,
            'match_score': 0,
            'status': 'pending',
            'applied_at': datetime.utcnow()
        }
        result = candidates_collection.insert_one(candidate)
        return str(result.inserted_id)

    @staticmethod
    def find_all():
        return list(candidates_collection.find())

    @staticmethod
    def find_by_job(job_id):
        return list(candidates_collection.find({'job_id': job_id}))

    @staticmethod
    def find_by_id(candidate_id):
        try:
            return candidates_collection.find_one({'_id': ObjectId(candidate_id)})
        except:
            return None

    @staticmethod
    def update(candidate_id, data):
        return candidates_collection.update_one({'_id': ObjectId(candidate_id)}, {'$set': data})

    @staticmethod
    def delete(candidate_id):
        return candidates_collection.delete_one({'_id': ObjectId(candidate_id)})
