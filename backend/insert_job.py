"""
Job Insertion Functions for MongoDB

This module provides functions to insert job postings into the MongoDB jobs collection.
"""

from db import db
from datetime import datetime
from bson import ObjectId

# Get jobs collection
jobs_collection = db["jobs"]

def insert_job(job_title, description, required_skills, experience, location, salary_range="", status="open", created_by=None):
    """
    Insert a new job posting into the jobs collection.
    
    Args:
        job_title (str): Job title/position
        description (str): Detailed job description
        required_skills (str): Required skills (comma-separated or text)
        experience (str): Required experience (e.g., "2-3 years")
        location (str): Job location
        salary_range (str): Salary range (optional)
        status (str): Job status - "open" or "closed" (default: "open")
        created_by (str): User ID who created the job (optional)
    
    Returns:
        str: Inserted job ID as string
        
    Raises:
        ValueError: If validation fails
        Exception: If insertion fails
    
    Example:
        job_id = insert_job(
            job_title="Senior Python Developer",
            description="We are looking for...",
            required_skills="Python, Flask, MongoDB",
            experience="3-5 years",
            location="Remote"
        )
        print(f"Job created with ID: {job_id}")
    """
    
    # Validate inputs
    if not job_title or not job_title.strip():
        raise ValueError("Job title is required")
    
    if len(job_title.strip()) < 3:
        raise ValueError("Job title must be at least 3 characters")
    
    if not description or not description.strip():
        raise ValueError("Description is required")
    
    if len(description.strip()) < 10:
        raise ValueError("Description must be at least 10 characters")
    
    if not required_skills or not required_skills.strip():
        raise ValueError("Required skills are required")
    
    if not experience or not experience.strip():
        raise ValueError("Experience is required")
    
    if not location or not location.strip():
        raise ValueError("Location is required")
    
    valid_statuses = ["open", "closed"]
    if status not in valid_statuses:
        raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
    
    # Create job document
    job = {
        "job_title": job_title.strip(),
        "description": description.strip(),
        "required_skills": required_skills.strip(),
        "experience": experience.strip(),
        "location": location.strip(),
        "salary_range": salary_range.strip() if salary_range else "",
        "status": status,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Add created_by if provided
    if created_by:
        try:
            job["created_by"] = ObjectId(created_by)
        except:
            raise ValueError("Invalid created_by user ID")
    
    # Insert into database using insert_one()
    result = jobs_collection.insert_one(job)
    
    # Return inserted ID as string
    return str(result.inserted_id)


def insert_job_simple(job_title, description, required_skills, experience, location):
    """
    Simple version - Insert job without validation.
    
    Args:
        job_title (str): Job title
        description (str): Job description
        required_skills (str): Required skills
        experience (str): Required experience
        location (str): Job location
    
    Returns:
        str: Inserted job ID as string
    
    Example:
        job_id = insert_job_simple(
            "Python Developer",
            "Looking for Python developer",
            "Python, Flask",
            "2 years",
            "Remote"
        )
    """
    
    job = {
        "job_title": job_title,
        "description": description,
        "required_skills": required_skills,
        "experience": experience,
        "location": location,
        "status": "open",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = jobs_collection.insert_one(job)
    return str(result.inserted_id)


def insert_multiple_jobs(jobs_list):
    """
    Insert multiple jobs at once.
    
    Args:
        jobs_list (list): List of job dictionaries
        
    Returns:
        list: List of inserted job IDs as strings
    
    Example:
        jobs = [
            {
                "job_title": "Python Developer",
                "description": "Looking for Python developer",
                "required_skills": "Python, Flask",
                "experience": "2 years",
                "location": "Remote"
            },
            {
                "job_title": "React Developer",
                "description": "Looking for React developer",
                "required_skills": "React, JavaScript",
                "experience": "3 years",
                "location": "New York"
            }
        ]
        job_ids = insert_multiple_jobs(jobs)
    """
    
    # Add timestamps and status to each job
    for job in jobs_list:
        job["status"] = job.get("status", "open")
        job["created_at"] = datetime.utcnow()
        job["updated_at"] = datetime.utcnow()
    
    # Insert all jobs
    result = jobs_collection.insert_many(jobs_list)
    
    # Return list of IDs as strings
    return [str(id) for id in result.inserted_ids]


def create_remote_job(job_title, description, required_skills, experience, salary_range=""):
    """
    Create a remote job posting (convenience function).
    
    Args:
        job_title (str): Job title
        description (str): Job description
        required_skills (str): Required skills
        experience (str): Required experience
        salary_range (str): Salary range (optional)
    
    Returns:
        str: Inserted job ID
    
    Example:
        job_id = create_remote_job(
            "Senior Python Developer",
            "We are looking for...",
            "Python, Flask, MongoDB",
            "3-5 years",
            "$80,000 - $120,000"
        )
    """
    return insert_job(
        job_title=job_title,
        description=description,
        required_skills=required_skills,
        experience=experience,
        location="Remote",
        salary_range=salary_range
    )


def get_all_jobs():
    """
    Get all jobs from the database.
    
    Returns:
        list: List of all job documents
    """
    return list(jobs_collection.find())


def get_open_jobs():
    """
    Get all open jobs.
    
    Returns:
        list: List of open job documents
    """
    return list(jobs_collection.find({"status": "open"}))


def get_job_by_id(job_id):
    """
    Get a job by ID.
    
    Args:
        job_id (str): Job ID
    
    Returns:
        dict: Job document or None
    """
    try:
        return jobs_collection.find_one({"_id": ObjectId(job_id)})
    except:
        return None


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("JOB INSERTION EXAMPLES")
    print("="*70)
    
    try:
        # Example 1: Insert a single job
        print("\n1. Inserting Python Developer job...")
        job_id = insert_job(
            job_title="Senior Python Developer",
            description="We are looking for an experienced Python developer with strong backend skills. The ideal candidate will have experience with Flask, MongoDB, and REST APIs.",
            required_skills="Python, Flask, MongoDB, REST API, Docker, AWS",
            experience="3-5 years",
            location="Remote",
            salary_range="$80,000 - $120,000"
        )
        print(f"   ✓ Job created with ID: {job_id}")
        
    except ValueError as e:
        print(f"   ✗ Validation error: {e}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    try:
        # Example 2: Insert a React Developer job
        print("\n2. Inserting React Developer job...")
        job_id = insert_job(
            job_title="Frontend React Developer",
            description="Looking for a talented React developer to join our team. You will be responsible for building user interfaces and working closely with our design team.",
            required_skills="React, JavaScript, TypeScript, HTML, CSS, Redux",
            experience="2-4 years",
            location="New York, NY",
            salary_range="$70,000 - $100,000"
        )
        print(f"   ✓ Job created with ID: {job_id}")
        
    except ValueError as e:
        print(f"   ✗ Validation error: {e}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    try:
        # Example 3: Insert a remote job using convenience function
        print("\n3. Inserting remote job...")
        job_id = create_remote_job(
            job_title="Full Stack Developer",
            description="We need a full stack developer who can work on both frontend and backend. Experience with modern web technologies is required.",
            required_skills="Python, React, Node.js, MongoDB, PostgreSQL",
            experience="4-6 years",
            salary_range="$90,000 - $130,000"
        )
        print(f"   ✓ Remote job created with ID: {job_id}")
        
    except ValueError as e:
        print(f"   ✗ Validation error: {e}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Display all jobs
    print("\n" + "="*70)
    print("ALL JOBS IN DATABASE")
    print("="*70)
    
    all_jobs = get_all_jobs()
    print(f"\nTotal jobs: {len(all_jobs)}\n")
    
    for job in all_jobs:
        print(f"ID: {job['_id']}")
        print(f"Title: {job['job_title']}")
        print(f"Location: {job['location']}")
        print(f"Experience: {job['experience']}")
        print(f"Status: {job['status']}")
        print(f"Created: {job['created_at']}")
        print("-" * 70)
    
    print()
