from pymongo import MongoClient
from bson import ObjectId
import bcrypt
from database import get_collection

users_collection = get_collection('users')

class User:
    @staticmethod
    def create(email, password, name, role='Candidate'):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = {
            'email': email,
            'password': hashed,
            'name': name,
            'role': role
        }
        result = users_collection.insert_one(user)
        return str(result.inserted_id)

    @staticmethod
    def find_by_email(email):
        return users_collection.find_one({'email': email})

    @staticmethod
    def verify_password(stored_password, provided_password):
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)
