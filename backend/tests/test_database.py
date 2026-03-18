"""
MongoDB Connection Test Script

This script tests the MongoDB connection and verifies the database setup
for the AI HR Management System.
"""

from database import db_instance, get_database, get_collection
from config import Config

def test_connection():
    """Test MongoDB connection."""
    print("\n" + "="*60)
    print("MONGODB CONNECTION TEST")
    print("="*60)
    
    try:
        # Get database instance
        db = get_database()
        
        print(f"\n✓ Connected to MongoDB successfully")
        print(f"✓ Database Name: {Config.DATABASE_NAME}")
        print(f"✓ Connection URI: {Config.MONGO_URI.split('@')[-1] if '@' in Config.MONGO_URI else Config.MONGO_URI}")
        
        # List collections
        collections = db.list_collection_names()
        print(f"\n✓ Available Collections: {len(collections)}")
        for collection in collections:
            print(f"  - {collection}")
        
        # Get database stats
        print("\n" + "-"*60)
        print("DATABASE STATISTICS")
        print("-"*60)
        stats = db_instance.get_stats()
        for key, value in stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Connection failed: {str(e)}")
        return False

def test_collections():
    """Test access to all collections."""
    print("\n" + "="*60)
    print("COLLECTIONS ACCESS TEST")
    print("="*60)
    
    collections_to_test = ['users', 'jobs', 'candidates']
    
    for collection_name in collections_to_test:
        try:
            collection = get_collection(collection_name)
            count = collection.count_documents({})
            print(f"\n✓ Collection '{collection_name}': {count} documents")
            
            # Show indexes
            indexes = collection.list_indexes()
            print(f"  Indexes:")
            for index in indexes:
                print(f"    - {index['name']}")
                
        except Exception as e:
            print(f"\n✗ Error accessing '{collection_name}': {str(e)}")

def test_crud_operations():
    """Test basic CRUD operations."""
    print("\n" + "="*60)
    print("CRUD OPERATIONS TEST")
    print("="*60)
    
    try:
        # Test with jobs collection
        jobs_collection = get_collection('jobs')
        
        # Create (Insert)
        test_job = {
            'job_title': 'Test Job - MongoDB Connection Test',
            'description': 'This is a test job',
            'required_skills': 'Testing',
            'location': 'Test Location',
            'status': 'test'
        }
        
        result = jobs_collection.insert_one(test_job)
        print(f"\n✓ CREATE: Inserted test document with ID: {result.inserted_id}")
        
        # Read
        found_job = jobs_collection.find_one({'_id': result.inserted_id})
        print(f"✓ READ: Found document: {found_job['job_title']}")
        
        # Update
        jobs_collection.update_one(
            {'_id': result.inserted_id},
            {'$set': {'status': 'test_updated'}}
        )
        updated_job = jobs_collection.find_one({'_id': result.inserted_id})
        print(f"✓ UPDATE: Updated status to: {updated_job['status']}")
        
        # Delete
        jobs_collection.delete_one({'_id': result.inserted_id})
        deleted_job = jobs_collection.find_one({'_id': result.inserted_id})
        if deleted_job is None:
            print(f"✓ DELETE: Test document deleted successfully")
        
        return True
        
    except Exception as e:
        print(f"\n✗ CRUD operations failed: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("AI HR MANAGEMENT SYSTEM - DATABASE TEST SUITE")
    print("="*60)
    
    # Test 1: Connection
    connection_ok = test_connection()
    
    if connection_ok:
        # Test 2: Collections
        test_collections()
        
        # Test 3: CRUD Operations
        test_crud_operations()
    
    print("\n" + "="*60)
    print("TEST SUITE COMPLETED")
    print("="*60)
    print("\nDatabase Configuration:")
    print(f"  Database Name: {Config.DATABASE_NAME}")
    print(f"  Collections: users, jobs, candidates")
    print(f"  Connection: {Config.MONGO_URI}")
    print("\n")

if __name__ == "__main__":
    main()
