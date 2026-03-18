"""
User Insertion Functions for MongoDB

This module provides functions to insert users into the MongoDB users collection.
"""

from db import db
from datetime import datetime
import bcrypt

# Get users collection
users_collection = db["users"]

def insert_user(name, email, password, role="Candidate"):
    """
    Insert a new user into the users collection.
    
    Args:
        name (str): User's full name
        email (str): User's email address
        password (str): User's password (will be hashed)
        role (str): User role - "HR", "Candidate", or "Admin" (default: "Candidate")
    
    Returns:
        str: Inserted user ID as string
        
    Raises:
        ValueError: If validation fails
        Exception: If insertion fails
    
    Example:
        user_id = insert_user("John Doe", "john@example.com", "password123", "HR")
        print(f"User created with ID: {user_id}")
    """
    
    # Validate inputs
    if not name or not name.strip():
        raise ValueError("Name is required")
    
    if not email or not email.strip():
        raise ValueError("Email is required")
    
    if not password or len(password) < 6:
        raise ValueError("Password must be at least 6 characters")
    
    valid_roles = ["HR", "Candidate", "Admin"]
    if role not in valid_roles:
        raise ValueError(f"Role must be one of: {', '.join(valid_roles)}")
    
    # Check if email already exists
    existing_user = users_collection.find_one({"email": email.lower()})
    if existing_user:
        raise ValueError(f"Email '{email}' already exists")
    
    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Create user document
    user = {
        "name": name.strip(),
        "email": email.lower().strip(),
        "password": hashed_password,
        "role": role,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Insert into database
    result = users_collection.insert_one(user)
    
    # Return inserted ID as string
    return str(result.inserted_id)


def insert_user_simple(name, email, password, role="Candidate"):
    """
    Simple version - Insert user without validation or password hashing.
    
    Args:
        name (str): User's full name
        email (str): User's email address
        password (str): User's password (plain text)
        role (str): User role (default: "Candidate")
    
    Returns:
        str: Inserted user ID as string
    
    Example:
        user_id = insert_user_simple("Jane Doe", "jane@example.com", "pass123")
    """
    
    user = {
        "name": name,
        "email": email,
        "password": password,
        "role": role,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = users_collection.insert_one(user)
    return str(result.inserted_id)


def insert_multiple_users(users_list):
    """
    Insert multiple users at once.
    
    Args:
        users_list (list): List of user dictionaries
        
    Returns:
        list: List of inserted user IDs as strings
    
    Example:
        users = [
            {"name": "User 1", "email": "user1@example.com", "password": "pass123", "role": "HR"},
            {"name": "User 2", "email": "user2@example.com", "password": "pass456", "role": "Candidate"}
        ]
        user_ids = insert_multiple_users(users)
    """
    
    # Add timestamps to each user
    for user in users_list:
        user["created_at"] = datetime.utcnow()
        user["updated_at"] = datetime.utcnow()
    
    # Insert all users
    result = users_collection.insert_many(users_list)
    
    # Return list of IDs as strings
    return [str(id) for id in result.inserted_ids]


def create_hr_user(name, email, password):
    """
    Create an HR user (convenience function).
    
    Args:
        name (str): User's full name
        email (str): User's email address
        password (str): User's password
    
    Returns:
        str: Inserted user ID
    
    Example:
        hr_id = create_hr_user("HR Manager", "hr@company.com", "secure123")
    """
    return insert_user(name, email, password, role="HR")


def create_candidate_user(name, email, password):
    """
    Create a Candidate user (convenience function).
    
    Args:
        name (str): User's full name
        email (str): User's email address
        password (str): User's password
    
    Returns:
        str: Inserted user ID
    
    Example:
        candidate_id = create_candidate_user("John Smith", "john@example.com", "pass123")
    """
    return insert_user(name, email, password, role="Candidate")


def create_admin_user(name, email, password):
    """
    Create an Admin user (convenience function).
    
    Args:
        name (str): User's full name
        email (str): User's email address
        password (str): User's password
    
    Returns:
        str: Inserted user ID
    
    Example:
        admin_id = create_admin_user("System Admin", "admin@company.com", "admin123")
    """
    return insert_user(name, email, password, role="Admin")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("USER INSERTION EXAMPLES")
    print("="*70)
    
    try:
        # Example 1: Insert a single user
        print("\n1. Inserting HR user...")
        user_id = insert_user(
            name="John Doe",
            email="john@example.com",
            password="password123",
            role="HR"
        )
        print(f"   ✓ User created with ID: {user_id}")
        
    except ValueError as e:
        print(f"   ✗ Validation error: {e}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    try:
        # Example 2: Insert a candidate
        print("\n2. Inserting Candidate user...")
        candidate_id = create_candidate_user(
            name="Jane Smith",
            email="jane@example.com",
            password="secure456"
        )
        print(f"   ✓ Candidate created with ID: {candidate_id}")
        
    except ValueError as e:
        print(f"   ✗ Validation error: {e}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    try:
        # Example 3: Insert an admin
        print("\n3. Inserting Admin user...")
        admin_id = create_admin_user(
            name="System Admin",
            email="admin@example.com",
            password="admin789"
        )
        print(f"   ✓ Admin created with ID: {admin_id}")
        
    except ValueError as e:
        print(f"   ✗ Validation error: {e}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    try:
        # Example 4: Insert multiple users
        print("\n4. Inserting multiple users...")
        users = [
            {
                "name": "User One",
                "email": "user1@example.com",
                "password": bcrypt.hashpw("pass1".encode('utf-8'), bcrypt.gensalt()),
                "role": "Candidate"
            },
            {
                "name": "User Two",
                "email": "user2@example.com",
                "password": bcrypt.hashpw("pass2".encode('utf-8'), bcrypt.gensalt()),
                "role": "HR"
            }
        ]
        user_ids = insert_multiple_users(users)
        print(f"   ✓ Created {len(user_ids)} users")
        for i, uid in enumerate(user_ids, 1):
            print(f"     - User {i}: {uid}")
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Display all users
    print("\n" + "="*70)
    print("ALL USERS IN DATABASE")
    print("="*70)
    
    all_users = list(users_collection.find())
    print(f"\nTotal users: {len(all_users)}\n")
    
    for user in all_users:
        print(f"ID: {user['_id']}")
        print(f"Name: {user['name']}")
        print(f"Email: {user['email']}")
        print(f"Role: {user['role']}")
        print(f"Created: {user['created_at']}")
        print("-" * 70)
    
    print()
