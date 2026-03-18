"""
MongoDB Collections Schema for AI HR Management System

This file defines the structure and fields for all collections.
"""

from datetime import datetime
from bson import ObjectId

# ============================================================================
# COLLECTION SCHEMAS
# ============================================================================

# 1. USERS COLLECTION
users_schema = {
    "_id": ObjectId,              # Auto-generated unique identifier
    "name": str,                  # User's full name
    "email": str,                 # User's email (unique)
    "password": str,              # Hashed password
    "role": str,                  # User role: "HR", "Candidate", "Admin"
    "created_at": datetime,       # Account creation timestamp
    "updated_at": datetime        # Last update timestamp
}

users_example = {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "$2b$12$hashed_password_here",
    "role": "HR",
    "created_at": datetime.utcnow(),
    "updated_at": datetime.utcnow()
}

# 2. JOBS COLLECTION
jobs_schema = {
    "_id": ObjectId,              # Auto-generated unique identifier
    "job_title": str,             # Job title/position
    "description": str,           # Detailed job description
    "required_skills": str,       # Required skills (comma-separated or text)
    "experience": str,            # Required experience (e.g., "2-3 years")
    "location": str,              # Job location
    "salary_range": str,          # Salary range (optional)
    "status": str,                # Job status: "open", "closed"
    "created_by": ObjectId,       # User ID who created the job
    "created_at": datetime,       # Job posting timestamp
    "updated_at": datetime        # Last update timestamp
}

jobs_example = {
    "job_title": "Senior Python Developer",
    "description": "We are looking for an experienced Python developer...",
    "required_skills": "Python, Flask, MongoDB, REST API, Docker",
    "experience": "3-5 years",
    "location": "Remote",
    "salary_range": "$80,000 - $120,000",
    "status": "open",
    "created_by": ObjectId("507f1f77bcf86cd799439011"),
    "created_at": datetime.utcnow(),
    "updated_at": datetime.utcnow()
}

# 3. CANDIDATES COLLECTION
candidates_schema = {
    "_id": ObjectId,              # Auto-generated unique identifier
    "candidate_name": str,        # Candidate's full name
    "email": str,                 # Candidate's email
    "phone": str,                 # Candidate's phone number
    "resume_file": str,           # Path to uploaded resume file
    "resume_text": str,           # Extracted text from resume
    "skills": list,               # List of skills (array of strings)
    "experience": str,            # Years of experience
    "education": str,             # Educational background (optional)
    "created_at": datetime,       # Registration timestamp
    "updated_at": datetime        # Last update timestamp
}

candidates_example = {
    "candidate_name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "+1234567890",
    "resume_file": "uploads/20240115_143025_jane@example.com_resume.pdf",
    "resume_text": "Experienced Python developer with 5 years...",
    "skills": ["Python", "Flask", "MongoDB", "AWS", "Docker"],
    "experience": "5 years",
    "education": "Bachelor of Science in Computer Science",
    "created_at": datetime.utcnow(),
    "updated_at": datetime.utcnow()
}

# 4. APPLICATIONS COLLECTION
applications_schema = {
    "_id": ObjectId,              # Auto-generated unique identifier
    "candidate_id": ObjectId,     # Reference to candidates collection
    "job_id": ObjectId,           # Reference to jobs collection
    "match_score": float,         # AI-calculated match score (0-100)
    "status": str,                # Application status: "pending", "shortlisted", "interviewed", "rejected", "hired"
    "applied_at": datetime,       # Application submission timestamp
    "updated_at": datetime,       # Last status update timestamp
    "notes": str                  # HR notes (optional)
}

applications_example = {
    "candidate_id": ObjectId("507f1f77bcf86cd799439011"),
    "job_id": ObjectId("507f1f77bcf86cd799439012"),
    "match_score": 87.5,
    "status": "shortlisted",
    "applied_at": datetime.utcnow(),
    "updated_at": datetime.utcnow(),
    "notes": "Strong technical background, good communication skills"
}

# ============================================================================
# COLLECTION INDEXES
# ============================================================================

# Indexes for better query performance
indexes = {
    "users": [
        {"keys": [("email", 1)], "unique": True},
        {"keys": [("role", 1)]},
        {"keys": [("created_at", -1)]}
    ],
    "jobs": [
        {"keys": [("status", 1)]},
        {"keys": [("created_at", -1)]},
        {"keys": [("job_title", "text"), ("description", "text")]}
    ],
    "candidates": [
        {"keys": [("email", 1)], "unique": True},
        {"keys": [("created_at", -1)]},
        {"keys": [("skills", 1)]}
    ],
    "applications": [
        {"keys": [("candidate_id", 1)]},
        {"keys": [("job_id", 1)]},
        {"keys": [("match_score", -1)]},
        {"keys": [("status", 1)]},
        {"keys": [("applied_at", -1)]},
        {"keys": [("candidate_id", 1), ("job_id", 1)], "unique": True}
    ]
}

# ============================================================================
# VALIDATION RULES
# ============================================================================

validation_rules = {
    "users": {
        "required_fields": ["name", "email", "password", "role"],
        "valid_roles": ["HR", "Candidate", "Admin"]
    },
    "jobs": {
        "required_fields": ["job_title", "description", "required_skills", "experience", "location"],
        "valid_statuses": ["open", "closed"]
    },
    "candidates": {
        "required_fields": ["candidate_name", "email", "resume_file", "skills"]
    },
    "applications": {
        "required_fields": ["candidate_id", "job_id", "match_score", "status"],
        "valid_statuses": ["pending", "shortlisted", "interviewed", "rejected", "hired"]
    }
}

# ============================================================================
# COLLECTION DESCRIPTIONS
# ============================================================================

collections_info = {
    "users": {
        "description": "Stores user accounts for HR personnel, candidates, and admins",
        "relationships": [
            "jobs.created_by -> users._id"
        ]
    },
    "jobs": {
        "description": "Stores job postings created by HR",
        "relationships": [
            "applications.job_id -> jobs._id"
        ]
    },
    "candidates": {
        "description": "Stores candidate profiles and resume information",
        "relationships": [
            "applications.candidate_id -> candidates._id"
        ]
    },
    "applications": {
        "description": "Stores job applications with AI match scores",
        "relationships": [
            "applications.candidate_id -> candidates._id",
            "applications.job_id -> jobs._id"
        ]
    }
}

# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'users_schema',
    'jobs_schema',
    'candidates_schema',
    'applications_schema',
    'indexes',
    'validation_rules',
    'collections_info'
]
