# MongoDB Setup Guide for Flask Backend

## ✅ Current Status

PyMongo is already included in `requirements.txt`:
```
pymongo==4.6.1
```

## Installation Steps

### 1. Install Python Dependencies

```bash
# Navigate to backend directory
cd backend

# Install all dependencies including PyMongo
pip install -r requirements.txt
```

### 2. Install MongoDB

#### Windows:
```bash
# Download MongoDB Community Server from:
https://www.mongodb.com/try/download/community

# Or use Chocolatey:
choco install mongodb

# Start MongoDB service:
net start MongoDB
```

#### macOS:
```bash
# Using Homebrew:
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB:
brew services start mongodb-community
```

#### Linux (Ubuntu/Debian):
```bash
# Import MongoDB public key:
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Add MongoDB repository:
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Install MongoDB:
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start MongoDB:
sudo systemctl start mongod
sudo systemctl enable mongod
```

### 3. Verify MongoDB Installation

```bash
# Check if MongoDB is running:
mongosh

# Or check the service status:
# Windows:
sc query MongoDB

# macOS/Linux:
sudo systemctl status mongod
```

### 4. Test Database Connection

```bash
# Run the test script:
python test_db.py
```

Expected output:
```
✓ Connected to MongoDB: ai_hr_system
✓ Import successful
✓ Connection successful
✓ Database: ai_hr_system
✓ ALL TESTS PASSED
```

## MongoDB Configuration

### Connection Details:
- **URL:** `mongodb://localhost:27017/`
- **Database:** `ai_hr_system`
- **Collections:** `users`, `jobs`, `candidates`

### Connection File: `db.py`

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ai_hr_system"]
```

## Usage in Your Code

### Import Database:
```python
from db import db
```

### Access Collections:
```python
# Users collection
users = db["users"]

# Jobs collection
jobs = db["jobs"]

# Candidates collection
candidates = db["candidates"]
```

### CRUD Operations:

#### Create (Insert):
```python
from db import db

users = db["users"]
result = users.insert_one({
    "name": "John Doe",
    "email": "john@example.com",
    "role": "HR"
})
user_id = result.inserted_id
```

#### Read (Find):
```python
from db import db

users = db["users"]

# Find all
all_users = list(users.find())

# Find one
user = users.find_one({"email": "john@example.com"})

# Find with filter
hr_users = list(users.find({"role": "HR"}))
```

#### Update:
```python
from db import db
from bson import ObjectId

users = db["users"]

users.update_one(
    {"_id": ObjectId(user_id)},
    {"$set": {"name": "Jane Doe"}}
)
```

#### Delete:
```python
from db import db
from bson import ObjectId

users = db["users"]

users.delete_one({"_id": ObjectId(user_id)})
```

## Verify Setup

### 1. Check PyMongo Installation:
```bash
python -c "import pymongo; print(pymongo.__version__)"
```

Expected output: `4.6.1`

### 2. Check MongoDB Connection:
```bash
python -c "from db import db; print(db.name)"
```

Expected output: `ai_hr_system`

### 3. Run Full Test:
```bash
python test_db.py
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pymongo'"
**Solution:**
```bash
pip install pymongo
```

### Issue: "ServerSelectionTimeoutError"
**Solution:**
- Make sure MongoDB is running
- Check if MongoDB is listening on port 27017
```bash
# Windows:
net start MongoDB

# macOS:
brew services start mongodb-community

# Linux:
sudo systemctl start mongod
```

### Issue: "Connection refused"
**Solution:**
- Verify MongoDB is running: `mongosh`
- Check MongoDB logs
- Ensure port 27017 is not blocked by firewall

### Issue: Database not created
**Solution:**
- MongoDB creates databases automatically on first write operation
- Insert a document to create the database:
```python
from db import db
db["users"].insert_one({"test": "data"})
```

## MongoDB GUI Tools (Optional)

### MongoDB Compass (Official GUI):
```bash
# Download from:
https://www.mongodb.com/try/download/compass
```

### Studio 3T:
```bash
# Download from:
https://studio3t.com/download/
```

### Robo 3T:
```bash
# Download from:
https://robomongo.org/download
```

## Project Structure

```
backend/
├── db.py                    # MongoDB connection
├── requirements.txt         # Includes pymongo==4.6.1
├── test_db.py              # Test database connection
├── models/
│   ├── user_model.py       # Uses: from db import db
│   ├── job_model.py        # Uses: from db import db
│   └── candidate_model.py  # Uses: from db import db
├── routes/
│   ├── auth_routes.py      # Uses: from db import db
│   ├── job_routes.py       # Uses: from db import db
│   └── candidate_routes.py # Uses: from db import db
└── services/
    ├── job_service.py      # Uses: from db import db
    └── candidate_service.py # Uses: from db import db
```

## Quick Start Commands

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start MongoDB
# Windows:
net start MongoDB

# macOS:
brew services start mongodb-community

# Linux:
sudo systemctl start mongod

# 3. Test connection
python test_db.py

# 4. Run Flask app
python app.py
```

## Environment Variables (Optional)

Create `.env` file for configuration:
```env
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=ai_hr_system
```

Update `db.py` to use environment variables:
```python
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "ai_hr_system")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
```

## Summary

✅ **PyMongo** is already in `requirements.txt` (version 4.6.1)
✅ **db.py** connection module is created
✅ **test_db.py** test script is ready
✅ **MongoDB** needs to be installed and running locally
✅ **Database** `ai_hr_system` will be created automatically

## Next Steps

1. Install MongoDB on your system
2. Start MongoDB service
3. Run `pip install -r requirements.txt`
4. Test connection with `python test_db.py`
5. Start using MongoDB in your Flask app!

## Support

For issues:
- MongoDB Documentation: https://docs.mongodb.com/
- PyMongo Documentation: https://pymongo.readthedocs.io/
- MongoDB Community: https://www.mongodb.com/community/forums/
