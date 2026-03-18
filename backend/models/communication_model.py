from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from database import get_collection

communications_collection = get_collection('communications')

class Communication:
    @staticmethod
    def create(candidate_id, candidate_email, template_type, subject, message, scheduled_date=None, metadata=None):
        communication = {
            'candidate_id': candidate_id,
            'candidate_email': candidate_email,
            'template_type': template_type,
            'subject': subject,
            'message': message,
            'scheduled_date': scheduled_date,
            'sent_at': datetime.utcnow(),
            'status': 'sent',
            'metadata': metadata or {},
            'created_at': datetime.utcnow()
        }
        result = communications_collection.insert_one(communication)
        return str(result.inserted_id)

    @staticmethod
    def find_by_candidate(candidate_id):
        return list(communications_collection.find({'candidate_id': candidate_id}).sort('created_at', -1))

    @staticmethod
    def find_all():
        return list(communications_collection.find().sort('created_at', -1))

    @staticmethod
    def find_by_id(communication_id):
        try:
            return communications_collection.find_one({'_id': ObjectId(communication_id)})
        except:
            return None

    @staticmethod
    def update(communication_id, data):
        return communications_collection.update_one({'_id': ObjectId(communication_id)}, {'$set': data})

    @staticmethod
    def delete(communication_id):
        return communications_collection.delete_one({'_id': ObjectId(communication_id)})
