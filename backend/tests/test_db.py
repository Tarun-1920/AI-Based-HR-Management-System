"""
Test script for db.py MongoDB connection module.

Run this script to verify that db.py is working correctly.
"""

def test_db_connection():
    """Test database connection."""
    print("\n" + "="*60)
    print("TESTING DB.PY - MongoDB Connection Module")
    print("="*60)
    
    try:
        # Import db module
        print("\n1. Importing db module...")
        from db import db, get_db
        print("   ✓ Import successful")
        
        # Test connection
        print("\n2. Testing database connection...")
        db.command('ping')
        print("   ✓ Connection successful")
        
        # Get database name
        print("\n3. Checking database name...")
        print(f"   ✓ Database: {db.name}")
        
        # List collections
        print("\n4. Listing collections...")
        collections = db.list_collection_names()
        if collections:
            print(f"   ✓ Found {len(collections)} collections:")
            for col in collections:
                print(f"     - {col}")
        else:
            print("   ✓ No collections yet (database is empty)")
        
        # Test insert operation
        print("\n5. Testing insert operation...")
        test_collection = db['test_collection']
        result = test_collection.insert_one({'test': 'data', 'message': 'Hello from db.py'})
        print(f"   ✓ Insert successful, ID: {result.inserted_id}")
        
        # Test find operation
        print("\n6. Testing find operation...")
        doc = test_collection.find_one({'test': 'data'})
        if doc:
            print(f"   ✓ Find successful: {doc}")
        
        # Test delete operation
        print("\n7. Testing delete operation...")
        test_collection.delete_one({'test': 'data'})
        print("   ✓ Delete successful")
        
        # Clean up test collection
        db.drop_collection('test_collection')
        print("   ✓ Test collection cleaned up")
        
        # Get database stats
        print("\n8. Getting database statistics...")
        stats = db.command('dbstats')
        print(f"   ✓ Collections: {stats.get('collections', 0)}")
        print(f"   ✓ Data Size: {stats.get('dataSize', 0)} bytes")
        print(f"   ✓ Storage Size: {stats.get('storageSize', 0)} bytes")
        
        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED - db.py is working correctly!")
        print("="*60)
        
        print("\n📝 Usage in your code:")
        print("   from db import db")
        print("   users = db['users']")
        print("   users.insert_one({'name': 'John'})")
        print()
        
        return True
        
    except ImportError as e:
        print(f"\n✗ Import Error: {e}")
        print("   Make sure db.py is in the same directory")
        return False
        
    except Exception as e:
        print(f"\n✗ Test Failed: {e}")
        print("   Make sure MongoDB is running on localhost:27017")
        return False

if __name__ == '__main__':
    test_db_connection()
