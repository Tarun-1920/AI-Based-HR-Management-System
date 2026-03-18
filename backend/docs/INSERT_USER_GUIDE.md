# User Insertion Functions

## Overview

Functions to insert users into the MongoDB `users` collection using PyMongo's `insert_one()` method.

## Collection: users

### Fields:
- `name` - User's full name (string)
- `email` - User's email address (string, unique)
- `password` - Hashed password (string)
- `role` - User role: "HR", "Candidate", or "Admin" (string)
- `created_at` - Account creation timestamp (datetime)
- `updated_at` - Last update timestamp (datetime)

## Functions

### 1. insert_user()

Main function to insert a user with validation and password hashing.

```python
def insert_user(name, email, password, role="Candidate"):
    """
    Insert a new user into the users collection.
    
    Args:
        name (str): User's full name
        email (str): User's email address
        password (str): User's password (will be hashed)
        role (str): User role (default: "Candidate")
    
    Returns:
        str: Inserted user ID as string
    """
```

**Example:**
```python
from insert_user import insert_user

user_id = insert_user(
    name="John Doe",
    email="john@example.com",
    password="password123",
    role="HR"
)

print(f"User created with ID: {user_id}")
```

### 2. insert_user_simple()

Simple version without validation or password hashing.

```python
def insert_user_simple(name, email, password, role="Candidate"):
    """
    Simple version - Insert user without validation.
    
    Returns:
        str: Inserted user ID as string
    """
```

**Example:**
```python
user_id = insert_user_simple("Jane Doe", "jane@example.com", "pass123")
```

### 3. insert_multiple_users()

Insert multiple users at once.

```python
def insert_multiple_users(users_list):
    """
    Insert multiple users at once.
    
    Args:
        users_list (list): List of user dictionaries
        
    Returns:
        list: List of inserted user IDs as strings
    """
```

**Example:**
```python
users = [
    {"name": "User 1", "email": "user1@example.com", "password": "pass123", "role": "HR"},
    {"name": "User 2", "email": "user2@example.com", "password": "pass456", "role": "Candidate"}
]

user_ids = insert_multiple_users(users)
print(f"Created {len(user_ids)} users")
```

### 4. Convenience Functions

Quick functions for specific roles:

```python
# Create HR user
hr_id = create_hr_user("HR Manager", "hr@company.com", "secure123")

# Create Candidate user
candidate_id = create_candidate_user("John Smith", "john@example.com", "pass123")

# Create Admin user
admin_id = create_admin_user("System Admin", "admin@company.com", "admin123")
```

## Usage Examples

### Basic Usage:

```python
from db import db
from datetime import datetime
import bcrypt

users = db["users"]

def insert_user(name, email, password, role="Candidate"):
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
    
    # Insert using insert_one()
    result = users.insert_one(user)
    
    # Return inserted ID
    return str(result.inserted_id)

# Use the function
user_id = insert_user("John Doe", "john@example.com", "password123", "HR")
print(f"User ID: {user_id}")
```

### In Flask Route:

```python
from flask import Blueprint, request, jsonify
from insert_user import insert_user

user_bp = Blueprint('users', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    
    try:
        user_id = insert_user(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            role=data.get('role', 'Candidate')
        )
        
        return jsonify({
            'success': True,
            'message': 'User created successfully',
            'user_id': user_id
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to create user'
        }), 500
```

### Direct MongoDB Insert:

```python
from db import db
from datetime import datetime

users = db["users"]

# Create user document
user = {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "hashed_password_here",
    "role": "HR",
    "created_at": datetime.utcnow(),
    "updated_at": datetime.utcnow()
}

# Insert using insert_one()
result = users.insert_one(user)

# Get inserted ID
user_id = str(result.inserted_id)
print(f"Inserted user ID: {user_id}")
```

## Validation

The `insert_user()` function includes validation:

- ✅ Name is required and not empty
- ✅ Email is required and not empty
- ✅ Password must be at least 6 characters
- ✅ Role must be "HR", "Candidate", or "Admin"
- ✅ Email must be unique (checks for duplicates)
- ✅ Password is automatically hashed using bcrypt

## Return Value

All functions return the inserted user ID as a **string**.

```python
user_id = insert_user("John Doe", "john@example.com", "pass123", "HR")
# Returns: "507f1f77bcf86cd799439011"
```

## Error Handling

```python
try:
    user_id = insert_user("John Doe", "john@example.com", "pass123", "HR")
    print(f"Success! User ID: {user_id}")
    
except ValueError as e:
    print(f"Validation error: {e}")
    
except Exception as e:
    print(f"Database error: {e}")
```

## Testing

Run the test script:

```bash
python test_insert_user.py
```

Expected output:
```
1. Inserting HR user...
   ✓ Success! User ID: 507f1f77bcf86cd799439011

2. Inserting Candidate user...
   ✓ Success! User ID: 507f1f77bcf86cd799439012

3. Inserting Admin user...
   ✓ Success! User ID: 507f1f77bcf86cd799439013
```

## Complete Example

```python
from db import db
from datetime import datetime
import bcrypt

# Get users collection
users = db["users"]

def insert_user(name, email, password, role="Candidate"):
    """Insert a new user and return the user ID."""
    
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
    
    # Insert into database
    result = users.insert_one(user)
    
    # Return inserted ID as string
    return str(result.inserted_id)

# Example usage
if __name__ == "__main__":
    # Insert a user
    user_id = insert_user(
        name="John Doe",
        email="john@example.com",
        password="password123",
        role="HR"
    )
    
    print(f"User created with ID: {user_id}")
    
    # Verify insertion
    user = users.find_one({"_id": ObjectId(user_id)})
    print(f"User found: {user['name']} ({user['email']})")
```

## Summary

✅ **insert_user()** - Main function with validation and hashing
✅ **insert_user_simple()** - Simple version without validation
✅ **insert_multiple_users()** - Bulk insert
✅ **Convenience functions** - create_hr_user(), create_candidate_user(), create_admin_user()
✅ **Returns** - User ID as string
✅ **Uses** - PyMongo's insert_one() method
✅ **Includes** - Password hashing with bcrypt
✅ **Validates** - All required fields

Run `python test_insert_user.py` to test the functions!
