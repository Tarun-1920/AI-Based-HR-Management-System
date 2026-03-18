"""
Test Script for User Insertion

Simple examples of inserting users into MongoDB.
"""

from db import db
from datetime import datetime
import bcrypt

# Get users collection
users = db["users"]

def insert_user(name, email, password, role="Candidate"):
    """
    Insert a new user into the users collection.
    
    Args:
        name (str): User's full name
        email (str): User's email address
        password (str): User's password
        role (str): User role (default: "Candidate")
    
    Returns:
        str: Inserted user ID as string
    """
    
    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Create user document
    user = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "role": role,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Insert into database using insert_one()
    result = users.insert_one(user)
    
    # Return inserted ID as string
    return str(result.inserted_id)


# ============================================================================
# TEST EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("TESTING USER INSERTION")
    print("="*70)
    
    # Test 1: Insert HR user
    print("\n1. Inserting HR user...")
    try:
        user_id = insert_user(
            name="John Doe",
            email="john@example.com",
            password="password123",
            role="HR"
        )
        print(f"   ✓ Success! User ID: {user_id}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 2: Insert Candidate user
    print("\n2. Inserting Candidate user...")
    try:
        user_id = insert_user(
            name="Jane Smith",
            email="jane@example.com",
            password="secure456",
            role="Candidate"
        )
        print(f"   ✓ Success! User ID: {user_id}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 3: Insert Admin user
    print("\n3. Inserting Admin user...")
    try:
        user_id = insert_user(
            name="Admin User",
            email="admin@example.com",
            password="admin789",
            role="Admin"
        )
        print(f"   ✓ Success! User ID: {user_id}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Display all users
    print("\n" + "="*70)
    print("ALL USERS IN DATABASE")
    print("="*70)
    
    all_users = list(users.find())
    print(f"\nTotal users: {len(all_users)}\n")
    
    for user in all_users:
        print(f"Name: {user['name']}")
        print(f"Email: {user['email']}")
        print(f"Role: {user['role']}")
        print(f"ID: {user['_id']}")
        print("-" * 70)
    
    print()
