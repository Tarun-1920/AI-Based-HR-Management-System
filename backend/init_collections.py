"""
Initialize MongoDB Collections

This script creates all required collections and indexes for the
AI HR Management System.
"""

from db import db
from datetime import datetime

def create_collections():
    """Create all required collections."""
    
    print("\n" + "="*70)
    print("INITIALIZING MONGODB COLLECTIONS")
    print("="*70)
    
    collections = ["users", "jobs", "candidates", "applications"]
    
    existing_collections = db.list_collection_names()
    
    for collection in collections:
        if collection in existing_collections:
            print(f"✓ Collection '{collection}' already exists")
        else:
            db.create_collection(collection)
            print(f"✓ Created collection '{collection}'")

def create_indexes():
    """Create indexes for all collections."""
    
    print("\n" + "="*70)
    print("CREATING INDEXES")
    print("="*70)
    
    # Users collection indexes
    print("\n1. Users Collection:")
    try:
        db.users.create_index([("email", 1)], unique=True)
        print("   ✓ Created unique index on 'email'")
        
        db.users.create_index([("role", 1)])
        print("   ✓ Created index on 'role'")
        
        db.users.create_index([("created_at", -1)])
        print("   ✓ Created index on 'created_at'")
    except Exception as e:
        print(f"   ⚠ Warning: {e}")
    
    # Jobs collection indexes
    print("\n2. Jobs Collection:")
    try:
        db.jobs.create_index([("status", 1)])
        print("   ✓ Created index on 'status'")
        
        db.jobs.create_index([("created_at", -1)])
        print("   ✓ Created index on 'created_at'")
        
        db.jobs.create_index([("job_title", "text"), ("description", "text")])
        print("   ✓ Created text index on 'job_title' and 'description'")
    except Exception as e:
        print(f"   ⚠ Warning: {e}")
    
    # Candidates collection indexes
    print("\n3. Candidates Collection:")
    try:
        db.candidates.create_index([("email", 1)], unique=True)
        print("   ✓ Created unique index on 'email'")
        
        db.candidates.create_index([("created_at", -1)])
        print("   ✓ Created index on 'created_at'")
        
        db.candidates.create_index([("skills", 1)])
        print("   ✓ Created index on 'skills'")
    except Exception as e:
        print(f"   ⚠ Warning: {e}")
    
    # Applications collection indexes
    print("\n4. Applications Collection:")
    try:
        db.applications.create_index([("candidate_id", 1)])
        print("   ✓ Created index on 'candidate_id'")
        
        db.applications.create_index([("job_id", 1)])
        print("   ✓ Created index on 'job_id'")
        
        db.applications.create_index([("match_score", -1)])
        print("   ✓ Created index on 'match_score'")
        
        db.applications.create_index([("status", 1)])
        print("   ✓ Created index on 'status'")
        
        db.applications.create_index([("applied_at", -1)])
        print("   ✓ Created index on 'applied_at'")
        
        db.applications.create_index([("candidate_id", 1), ("job_id", 1)], unique=True)
        print("   ✓ Created unique compound index on 'candidate_id' and 'job_id'")
    except Exception as e:
        print(f"   ⚠ Warning: {e}")

def insert_sample_data():
    """Insert sample data for testing (optional)."""
    
    print("\n" + "="*70)
    print("INSERT SAMPLE DATA? (y/n)")
    print("="*70)
    
    choice = input("Enter choice: ").strip().lower()
    
    if choice != 'y':
        print("Skipped sample data insertion")
        return
    
    print("\nInserting sample data...")
    
    # Sample user
    try:
        user = {
            "name": "Admin User",
            "email": "admin@example.com",
            "password": "$2b$12$sample_hashed_password",
            "role": "Admin",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        user_result = db.users.insert_one(user)
        print(f"✓ Inserted sample user: {user_result.inserted_id}")
    except Exception as e:
        print(f"⚠ User already exists or error: {e}")
    
    # Sample job
    try:
        job = {
            "job_title": "Python Developer",
            "description": "Looking for an experienced Python developer",
            "required_skills": "Python, Flask, MongoDB",
            "experience": "2-3 years",
            "location": "Remote",
            "salary_range": "$60,000 - $80,000",
            "status": "open",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        job_result = db.jobs.insert_one(job)
        print(f"✓ Inserted sample job: {job_result.inserted_id}")
    except Exception as e:
        print(f"⚠ Error inserting job: {e}")
    
    # Sample candidate
    try:
        candidate = {
            "candidate_name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "resume_file": "uploads/sample_resume.pdf",
            "resume_text": "Experienced Python developer...",
            "skills": ["Python", "Flask", "MongoDB"],
            "experience": "3 years",
            "education": "Bachelor of Computer Science",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        candidate_result = db.candidates.insert_one(candidate)
        print(f"✓ Inserted sample candidate: {candidate_result.inserted_id}")
    except Exception as e:
        print(f"⚠ Candidate already exists or error: {e}")

def display_collections_info():
    """Display information about all collections."""
    
    print("\n" + "="*70)
    print("COLLECTIONS SUMMARY")
    print("="*70)
    
    collections = ["users", "jobs", "candidates", "applications"]
    
    for collection_name in collections:
        collection = db[collection_name]
        count = collection.count_documents({})
        indexes = collection.list_indexes()
        
        print(f"\n{collection_name.upper()}:")
        print(f"  Documents: {count}")
        print(f"  Indexes:")
        for index in indexes:
            print(f"    - {index['name']}")

def main():
    """Main initialization function."""
    
    print("\n" + "="*70)
    print("AI HR MANAGEMENT SYSTEM - DATABASE INITIALIZATION")
    print("="*70)
    print(f"\nDatabase: {db.name}")
    print(f"Collections: users, jobs, candidates, applications")
    
    try:
        # Create collections
        create_collections()
        
        # Create indexes
        create_indexes()
        
        # Insert sample data (optional)
        insert_sample_data()
        
        # Display summary
        display_collections_info()
        
        print("\n" + "="*70)
        print("✓ DATABASE INITIALIZATION COMPLETED SUCCESSFULLY")
        print("="*70)
        
        print("\n📝 Next Steps:")
        print("  1. Start your Flask application: python app.py")
        print("  2. Use the API endpoints to manage data")
        print("  3. View data using MongoDB Compass or mongosh")
        print()
        
    except Exception as e:
        print(f"\n✗ Initialization failed: {e}")
        print("Make sure MongoDB is running and accessible")

if __name__ == "__main__":
    main()
