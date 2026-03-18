# MongoDB Connection Module (db.py)

Simple and reusable MongoDB connection module for Flask backend projects.

## Configuration

- **Database Name:** `ai_hr_system`
- **Connection URL:** `mongodb://localhost:27017/`
- **Driver:** PyMongo

## Installation

```bash
pip install pymongo
```

## Usage

### Basic Import

```python
from db import db

# Access collections
users = db['users']
jobs = db['jobs']
candidates = db['candidates']
```

### In Routes

```python
from flask import Blueprint, jsonify
from db import db

user_bp = Blueprint('users', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    users_collection = db['users']
    users = list(users_collection.find())
    
    # Convert ObjectId to string
    for user in users:
        user['_id'] = str(user['_id'])
    
    return jsonify({'users': users}), 200
```

### In Models

```python
from db import db
from bson import ObjectId

class User:
    collection = db['users']
    
    @classmethod
    def create(cls, email, name):
        user = {'email': email, 'name': name}
        result = cls.collection.insert_one(user)
        return str(result.inserted_id)
    
    @classmethod
    def find_all(cls):
        return list(cls.collection.find())
    
    @classmethod
    def find_by_id(cls, user_id):
        return cls.collection.find_one({'_id': ObjectId(user_id)})
```

### In Services

```python
from db import db

class UserService:
    def __init__(self):
        self.collection = db['users']
    
    def get_all_users(self):
        return list(self.collection.find())
```

### In Flask App

```python
from flask import Flask
from db import db, close_db
import atexit

app = Flask(__name__)

# Register cleanup on shutdown
atexit.register(close_db)

@app.route('/health')
def health():
    try:
        db.command('ping')
        return {'status': 'healthy'}, 200
    except:
        return {'status': 'unhealthy'}, 500
```

## CRUD Operations

### Create (Insert)

```python
from db import db

users = db['users']

# Insert one
user_id = users.insert_one({
    'name': 'John Doe',
    'email': 'john@example.com'
}).inserted_id

# Insert many
users.insert_many([
    {'name': 'Jane', 'email': 'jane@example.com'},
    {'name': 'Bob', 'email': 'bob@example.com'}
])
```

### Read (Find)

```python
from db import db
from bson import ObjectId

users = db['users']

# Find all
all_users = list(users.find())

# Find one
user = users.find_one({'email': 'john@example.com'})

# Find by ID
user = users.find_one({'_id': ObjectId(user_id)})

# Find with filter
active_users = list(users.find({'status': 'active'}))

# Count
count = users.count_documents({})
```

### Update

```python
from db import db
from bson import ObjectId

users = db['users']

# Update one
users.update_one(
    {'_id': ObjectId(user_id)},
    {'$set': {'name': 'Jane Doe'}}
)

# Update many
users.update_many(
    {'status': 'inactive'},
    {'$set': {'status': 'active'}}
)
```

### Delete

```python
from db import db
from bson import ObjectId

users = db['users']

# Delete one
users.delete_one({'_id': ObjectId(user_id)})

# Delete many
users.delete_many({'status': 'inactive'})
```

## Collections

Access collections directly:

```python
from db import db

users = db['users']
jobs = db['jobs']
candidates = db['candidates']
```

## Testing

Run the test script to verify connection:

```bash
python test_db.py
```

Expected output:
```
✓ Connected to MongoDB successfully
✓ Database: ai_hr_system
✓ URL: mongodb://localhost:27017/
✓ ALL TESTS PASSED
```

## Error Handling

The module handles common errors:

- **ConnectionFailure** - MongoDB not running
- **ServerSelectionTimeoutError** - Cannot reach server
- **General exceptions** - Unexpected errors

If connection fails, the application will exit with an error message.

## Functions

### `connect_db()`
Establishes connection to MongoDB and returns database instance.

### `get_db()`
Returns the database instance. Creates connection if not exists.

### `close_db()`
Closes the database connection. Call on app shutdown.

## Example Project Structure

```
backend/
├── db.py                    # MongoDB connection module
├── app.py                   # Flask application
├── models/
│   ├── user_model.py       # Uses: from db import db
│   ├── job_model.py        # Uses: from db import db
│   └── candidate_model.py  # Uses: from db import db
├── routes/
│   ├── user_routes.py      # Uses: from db import db
│   ├── job_routes.py       # Uses: from db import db
│   └── candidate_routes.py # Uses: from db import db
└── services/
    ├── user_service.py     # Uses: from db import db
    └── job_service.py      # Uses: from db import db
```

## Troubleshooting

### MongoDB not running
```bash
# Start MongoDB
mongod

# Or on Windows
net start MongoDB
```

### Connection refused
- Check if MongoDB is running on port 27017
- Verify connection URL: `mongodb://localhost:27017/`

### Import error
- Make sure `db.py` is in the same directory or in Python path
- Install PyMongo: `pip install pymongo`

## Features

✅ Simple and clean API
✅ Automatic connection on import
✅ Error handling with clear messages
✅ Reusable across routes, models, and services
✅ Connection pooling (handled by PyMongo)
✅ Easy to test and debug

## Notes

- The connection is established when `db.py` is imported
- PyMongo handles connection pooling automatically
- The `db` instance is thread-safe
- Use `close_db()` when shutting down the application

## License

MIT
