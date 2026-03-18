"""
MongoDB Database Connection Module

This module provides centralized database connection and collection access
for the AI HR Management System using PyMongo.

Database: ai_hr_system
Collections: users, jobs, candidates
"""

from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config import Config
import sys

class Database:
    """MongoDB Database connection manager."""
    
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        """Singleton pattern to ensure single database connection."""
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize database connection."""
        if self._client is None:
            self.connect()
    
    def connect(self):
        """Establish connection to MongoDB."""
        try:
            # Create MongoDB client
            self._client = MongoClient(
                Config.MONGO_URI,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=10000,
                socketTimeoutMS=10000
            )
            
            # Test connection
            self._client.admin.command('ping')
            
            # Get database
            self._db = self._client[Config.DATABASE_NAME]
            
            print(f"Successfully connected to MongoDB")
            print(f"Database: {Config.DATABASE_NAME}")
            
            # Create indexes for better performance
            self._create_indexes()
            
        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            sys.exit(1)
        except ServerSelectionTimeoutError as e:
            print(f"MongoDB server not available: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error connecting to MongoDB: {e}")
            sys.exit(1)
    
    def _create_indexes(self):
        """Create indexes for collections to improve query performance."""
        try:
            # Users collection indexes
            self._db.users.create_index([("email", ASCENDING)], unique=True)
            
            # Jobs collection indexes
            self._db.jobs.create_index([("status", ASCENDING)])
            self._db.jobs.create_index([("created_at", DESCENDING)])
            
            # Candidates collection indexes
            self._db.candidates.create_index([("email", ASCENDING)])
            self._db.candidates.create_index([("job_id", ASCENDING)])
            self._db.candidates.create_index([("match_score", DESCENDING)])
            self._db.candidates.create_index([("status", ASCENDING)])
            self._db.candidates.create_index([("applied_at", DESCENDING)])
            
            print("Database indexes created successfully")
            
        except Exception as e:
            print(f"Warning: Could not create indexes: {e}")
    
    def get_db(self):
        """Get database instance."""
        if self._db is None:
            self.connect()
        return self._db
    
    def get_collection(self, collection_name):
        """
        Get a specific collection.
        
        Args:
            collection_name (str): Name of the collection
            
        Returns:
            Collection: MongoDB collection object
        """
        return self._db[collection_name]
    
    @property
    def users(self):
        """Get users collection."""
        return self._db.users
    
    @property
    def jobs(self):
        """Get jobs collection."""
        return self._db.jobs
    
    @property
    def candidates(self):
        """Get candidates collection."""
        return self._db.candidates
    
    def close(self):
        """Close database connection."""
        if self._client:
            self._client.close()
            print("MongoDB connection closed")
    
    def drop_database(self):
        """Drop the entire database (use with caution!)."""
        if self._client:
            self._client.drop_database(Config.DATABASE_NAME)
            print(f"Warning: Database '{Config.DATABASE_NAME}' dropped")
    
    def get_stats(self):
        """Get database statistics."""
        try:
            stats = self._db.command("dbstats")
            return {
                'database': stats.get('db'),
                'collections': stats.get('collections'),
                'data_size': f"{stats.get('dataSize', 0) / 1024 / 1024:.2f} MB",
                'storage_size': f"{stats.get('storageSize', 0) / 1024 / 1024:.2f} MB",
                'indexes': stats.get('indexes'),
                'index_size': f"{stats.get('indexSize', 0) / 1024 / 1024:.2f} MB"
            }
        except Exception as e:
            return {'error': str(e)}


# Global database instance
db_instance = Database()

def get_database():
    """
    Get database instance.
    
    Returns:
        Database: MongoDB database instance
    """
    return db_instance.get_db()

def get_collection(collection_name):
    """
    Get a specific collection.
    
    Args:
        collection_name (str): Name of the collection (users, jobs, candidates)
        
    Returns:
        Collection: MongoDB collection object
    """
    return db_instance.get_collection(collection_name)
