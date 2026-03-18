# MongoDB Collections Documentation

## Database: ai_hr_system

This document describes all collections and their schemas for the AI HR Management System.

---

## Collections Overview

| Collection | Purpose | Documents |
|------------|---------|-----------|
| **users** | User accounts (HR, Candidates, Admins) | User profiles |
| **jobs** | Job postings | Job listings |
| **candidates** | Candidate profiles | Resume data |
| **applications** | Job applications | Application tracking |

---

## 1. Users Collection

Stores user accounts for authentication and authorization.

### Schema:

```javascript
{
  _id: ObjectId,              // Auto-generated
  name: String,               // User's full name
  email: String,              // Unique email address
  password: String,           // Hashed password (bcrypt)
  role: String,               // "HR", "Candidate", or "Admin"
  created_at: Date,           // Account creation timestamp
  updated_at: Date            // Last update timestamp
}
```

### Example Document:

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "name": "John Doe",
  "email": "john@example.com",
  "password": "$2b$12$hashed_password_here",
  "role": "HR",
  "created_at": ISODate("2024-01-15T10:30:00Z"),
  "updated_at": ISODate("2024-01-15T10:30:00Z")
}
```

### Indexes:

- `email` (unique) - Fast user lookup by email
- `role` - Filter users by role
- `created_at` (descending) - Sort by registration date

### Valid Roles:

- `HR` - Human Resources personnel
- `Candidate` - Job applicants
- `Admin` - System administrators

---

## 2. Jobs Collection

Stores job postings created by HR.

### Schema:

```javascript
{
  _id: ObjectId,              // Auto-generated
  job_title: String,          // Job title/position
  description: String,        // Detailed job description
  required_skills: String,    // Required skills (comma-separated)
  experience: String,         // Required experience (e.g., "2-3 years")
  location: String,           // Job location
  salary_range: String,       // Salary range (optional)
  status: String,             // "open" or "closed"
  created_by: ObjectId,       // Reference to users._id
  created_at: Date,           // Job posting timestamp
  updated_at: Date            // Last update timestamp
}
```

### Example Document:

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439012"),
  "job_title": "Senior Python Developer",
  "description": "We are looking for an experienced Python developer with strong backend skills...",
  "required_skills": "Python, Flask, MongoDB, REST API, Docker, AWS",
  "experience": "3-5 years",
  "location": "Remote",
  "salary_range": "$80,000 - $120,000",
  "status": "open",
  "created_by": ObjectId("507f1f77bcf86cd799439011"),
  "created_at": ISODate("2024-01-15T10:30:00Z"),
  "updated_at": ISODate("2024-01-15T10:30:00Z")
}
```

### Indexes:

- `status` - Filter by open/closed jobs
- `created_at` (descending) - Sort by posting date
- `job_title, description` (text) - Full-text search

### Valid Statuses:

- `open` - Accepting applications
- `closed` - No longer accepting applications

---

## 3. Candidates Collection

Stores candidate profiles and resume information.

### Schema:

```javascript
{
  _id: ObjectId,              // Auto-generated
  candidate_name: String,     // Candidate's full name
  email: String,              // Unique email address
  phone: String,              // Phone number
  resume_file: String,        // Path to uploaded resume file
  resume_text: String,        // Extracted text from resume
  skills: Array,              // Array of skills
  experience: String,         // Years of experience
  education: String,          // Educational background (optional)
  created_at: Date,           // Registration timestamp
  updated_at: Date            // Last update timestamp
}
```

### Example Document:

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439013"),
  "candidate_name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "+1234567890",
  "resume_file": "uploads/20240115_143025_jane@example.com_resume.pdf",
  "resume_text": "Experienced Python developer with 5 years of experience in building scalable web applications...",
  "skills": ["Python", "Flask", "MongoDB", "AWS", "Docker", "REST API"],
  "experience": "5 years",
  "education": "Bachelor of Science in Computer Science",
  "created_at": ISODate("2024-01-15T10:30:00Z"),
  "updated_at": ISODate("2024-01-15T10:30:00Z")
}
```

### Indexes:

- `email` (unique) - Fast candidate lookup
- `created_at` (descending) - Sort by registration date
- `skills` - Filter by skills

---

## 4. Applications Collection

Stores job applications with AI-calculated match scores.

### Schema:

```javascript
{
  _id: ObjectId,              // Auto-generated
  candidate_id: ObjectId,     // Reference to candidates._id
  job_id: ObjectId,           // Reference to jobs._id
  match_score: Number,        // AI match score (0-100)
  status: String,             // Application status
  applied_at: Date,           // Application submission timestamp
  updated_at: Date,           // Last status update timestamp
  notes: String               // HR notes (optional)
}
```

### Example Document:

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439014"),
  "candidate_id": ObjectId("507f1f77bcf86cd799439013"),
  "job_id": ObjectId("507f1f77bcf86cd799439012"),
  "match_score": 87.5,
  "status": "shortlisted",
  "applied_at": ISODate("2024-01-15T10:30:00Z"),
  "updated_at": ISODate("2024-01-15T11:00:00Z"),
  "notes": "Strong technical background, excellent communication skills"
}
```

### Indexes:

- `candidate_id` - Find applications by candidate
- `job_id` - Find applications by job
- `match_score` (descending) - Sort by match score
- `status` - Filter by application status
- `applied_at` (descending) - Sort by application date
- `(candidate_id, job_id)` (unique compound) - Prevent duplicate applications

### Valid Statuses:

- `pending` - Application submitted, awaiting review
- `shortlisted` - Candidate shortlisted for interview
- `interviewed` - Interview completed
- `rejected` - Application rejected
- `hired` - Candidate hired

---

## Relationships

```
users (1) ----< jobs (many)
  |_id          |created_by

candidates (1) ----< applications (many)
  |_id                |candidate_id

jobs (1) ----< applications (many)
  |_id        |job_id
```

### Relationship Diagram:

```
┌─────────┐
│  users  │
└────┬────┘
     │ created_by
     ↓
┌─────────┐         ┌──────────────┐         ┌────────────┐
│  jobs   │←────────│ applications │────────→│ candidates │
└─────────┘  job_id └──────────────┘ candidate_id └────────────┘
```

---

## Queries Examples

### Find all open jobs:
```javascript
db.jobs.find({ status: "open" })
```

### Find applications for a specific job (sorted by match score):
```javascript
db.applications.find({ job_id: ObjectId("...") }).sort({ match_score: -1 })
```

### Find candidate by email:
```javascript
db.candidates.findOne({ email: "jane@example.com" })
```

### Find all HR users:
```javascript
db.users.find({ role: "HR" })
```

### Get top 10 candidates for a job:
```javascript
db.applications.find({ job_id: ObjectId("...") })
  .sort({ match_score: -1 })
  .limit(10)
```

### Count applications by status:
```javascript
db.applications.aggregate([
  { $group: { _id: "$status", count: { $sum: 1 } } }
])
```

---

## Initialization

Run the initialization script to create collections and indexes:

```bash
python init_collections.py
```

This will:
1. Create all collections
2. Create indexes for performance
3. Optionally insert sample data

---

## Validation Rules

### Users:
- `name`: Required, string
- `email`: Required, unique, valid email format
- `password`: Required, minimum 6 characters (hashed)
- `role`: Required, must be "HR", "Candidate", or "Admin"

### Jobs:
- `job_title`: Required, minimum 3 characters
- `description`: Required, minimum 10 characters
- `required_skills`: Required
- `experience`: Required
- `location`: Required
- `status`: Must be "open" or "closed"

### Candidates:
- `candidate_name`: Required, string
- `email`: Required, unique, valid email format
- `resume_file`: Required, path to file
- `skills`: Required, array of strings

### Applications:
- `candidate_id`: Required, valid ObjectId
- `job_id`: Required, valid ObjectId
- `match_score`: Required, number between 0-100
- `status`: Required, valid status value
- Unique constraint: One application per candidate per job

---

## Best Practices

1. **Always use ObjectId for references** between collections
2. **Index frequently queried fields** for better performance
3. **Use compound indexes** for queries with multiple conditions
4. **Store dates in UTC** using ISODate format
5. **Hash passwords** before storing (use bcrypt)
6. **Validate data** before insertion
7. **Use transactions** for operations affecting multiple collections
8. **Regular backups** of the database

---

## Maintenance

### View all collections:
```bash
mongosh
use ai_hr_system
show collections
```

### Check collection stats:
```javascript
db.users.stats()
db.jobs.stats()
db.candidates.stats()
db.applications.stats()
```

### View indexes:
```javascript
db.users.getIndexes()
db.jobs.getIndexes()
db.candidates.getIndexes()
db.applications.getIndexes()
```

### Backup database:
```bash
mongodump --db ai_hr_system --out backup/
```

### Restore database:
```bash
mongorestore --db ai_hr_system backup/ai_hr_system/
```

---

## Summary

✅ **4 Collections** defined with clear schemas
✅ **Indexes** created for optimal performance
✅ **Relationships** established between collections
✅ **Validation rules** documented
✅ **Sample data** available for testing
✅ **Initialization script** ready to use

Run `python init_collections.py` to set up your database!
