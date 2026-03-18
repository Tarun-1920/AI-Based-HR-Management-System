"""
Candidate Insertion Functions for MongoDB

This module provides functions to insert candidate information into the MongoDB candidates collection.
"""

from db import db
from datetime import datetime
from bson import ObjectId

# Get candidates collection
candidates_collection = db["candidates"]

def insert_candidate(candidate_name, email, resume_file, skills, job_id, phone="", resume_text="", experience=""):
    """
    Insert a new candidate into the candidates collection.
    
    Args:
        candidate_name (str): Candidate's full name
        email (str): Candidate's email address
        resume_file (str): Path to uploaded resume file
        skills (list): List of candidate skills
        job_id (str): Job ID the candidate is applying for
        phone (str): Phone number (optional)
        resume_text (str): Extracted text from resume (optional)
        experience (str): Years of experience (optional)
    
    Returns:
        str: Inserted candidate ID as string
        
    Raises:
        ValueError: If validation fails
        Exception: If insertion fails
    
    Example:
        candidate_id = insert_candidate(
            candidate_name="John Doe",
            email="john@example.com",
            resume_file="uploads/john_resume.pdf",
            skills=["Python", "Flask", "MongoDB"],
            job_id="507f1f77bcf86cd799439011"
        )
        print(f"Candidate created with ID: {candidate_id}")
    """
    
    # Validate inputs
    if not candidate_name or not candidate_name.strip():
        raise ValueError("Candidate name is required")
    
    if not email or not email.strip():
        raise ValueError("Email is required")
    
    # Basic email validation
    if '@' not in email or '.' not in email:
        raise ValueError("Invalid email format")
    
    if not resume_file or not resume_file.strip():
        raise ValueError("Resume file is required")
    
    if not skills or not isinstance(skills, list) or len(skills) == 0:
        raise ValueError("Skills are required and must be a list")
    
    if not job_id or not job_id.strip():
        raise ValueError("Job ID is required")
    
    # Validate job_id format
    try:
        ObjectId(job_id)
    except:
        raise ValueError("Invalid job ID format")
    
    # Check if candidate already applied for this job
    existing_application = candidates_collection.find_one({
        "email": email.lower().strip(),
        "job_id": job_id
    })
    
    if existing_application:
        raise ValueError(f"Candidate with email '{email}' has already applied for this job")
    
    # Create candidate document
    candidate = {
        "candidate_name": candidate_name.strip(),
        "email": email.lower().strip(),
        "phone": phone.strip() if phone else "",
        "resume_file": resume_file.strip(),
        "resume_text": resume_text.strip() if resume_text else "",
        "skills": skills,
        "experience": experience.strip() if experience else "",
        "job_id": job_id,
        "match_score": 0.0,  # Will be calculated by AI
        "status": "pending",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Insert into database using insert_one()
    result = candidates_collection.insert_one(candidate)
    
    # Return inserted ID as string
    return str(result.inserted_id)


def insert_candidate_simple(candidate_name, email, resume_file, skills, job_id):
    """
    Simple version - Insert candidate without validation.
    
    Args:
        candidate_name (str): Candidate's full name
        email (str): Candidate's email
        resume_file (str): Resume file path
        skills (list): List of skills
        job_id (str): Job ID
    
    Returns:
        str: Inserted candidate ID as string
    
    Example:
        candidate_id = insert_candidate_simple(
            "Jane Doe",
            "jane@example.com",
            "uploads/jane_resume.pdf",
            ["Python", "React"],
            "507f1f77bcf86cd799439011"
        )
    """
    
    candidate = {
        "candidate_name": candidate_name,
        "email": email,
        "resume_file": resume_file,
        "skills": skills,
        "job_id": job_id,
        "match_score": 0.0,
        "status": "pending",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = candidates_collection.insert_one(candidate)
    return str(result.inserted_id)


def save_candidate_on_resume_upload(candidate_name, email, phone, resume_file, resume_text, skills, job_id, experience=""):
    """
    Save candidate information when a resume is uploaded.
    This is the main function to use when processing resume uploads.
    
    Args:
        candidate_name (str): Candidate's full name
        email (str): Candidate's email
        phone (str): Candidate's phone number
        resume_file (str): Path to uploaded resume file
        resume_text (str): Extracted text from resume
        skills (list): List of extracted skills
        job_id (str): Job ID candidate is applying for
        experience (str): Years of experience (optional)
    
    Returns:
        str: Inserted candidate ID as string
    
    Example:
        # After resume upload and text extraction
        candidate_id = save_candidate_on_resume_upload(
            candidate_name="John Doe",
            email="john@example.com",
            phone="+1234567890",
            resume_file="uploads/20240115_john_resume.pdf",
            resume_text="Experienced Python developer with 5 years...",
            skills=["Python", "Flask", "MongoDB", "AWS"],
            job_id="507f1f77bcf86cd799439011",
            experience="5 years"
        )
    """
    
    return insert_candidate(
        candidate_name=candidate_name,
        email=email,
        resume_file=resume_file,
        skills=skills,
        job_id=job_id,
        phone=phone,
        resume_text=resume_text,
        experience=experience
    )


def get_all_candidates():
    """
    Get all candidates from the database.
    
    Returns:
        list: List of all candidate documents
    """
    return list(candidates_collection.find())


def get_candidates_by_job(job_id):
    """
    Get all candidates who applied for a specific job.
    
    Args:
        job_id (str): Job ID
    
    Returns:
        list: List of candidate documents
    """
    return list(candidates_collection.find({"job_id": job_id}))


def get_candidate_by_id(candidate_id):
    """
    Get a candidate by ID.
    
    Args:
        candidate_id (str): Candidate ID
    
    Returns:
        dict: Candidate document or None
    """
    try:
        return candidates_collection.find_one({"_id": ObjectId(candidate_id)})
    except:
        return None


def get_candidate_by_email(email):
    """
    Get a candidate by email.
    
    Args:
        email (str): Candidate email
    
    Returns:
        dict: Candidate document or None
    """
    return candidates_collection.find_one({"email": email.lower()})


def update_candidate_match_score(candidate_id, match_score):
    """
    Update candidate's AI match score.
    
    Args:
        candidate_id (str): Candidate ID
        match_score (float): Match score (0-100)
    
    Returns:
        bool: True if updated successfully
    """
    try:
        result = candidates_collection.update_one(
            {"_id": ObjectId(candidate_id)},
            {
                "$set": {
                    "match_score": match_score,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.matched_count > 0
    except:
        return False


def update_candidate_status(candidate_id, status):
    """
    Update candidate's application status.
    
    Args:
        candidate_id (str): Candidate ID
        status (str): New status (pending, shortlisted, interviewed, rejected, hired)
    
    Returns:
        bool: True if updated successfully
    """
    valid_statuses = ["pending", "shortlisted", "interviewed", "rejected", "hired"]
    
    if status not in valid_statuses:
        raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
    
    try:
        result = candidates_collection.update_one(
            {"_id": ObjectId(candidate_id)},
            {
                "$set": {
                    "status": status,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.matched_count > 0
    except:
        return False


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("CANDIDATE INSERTION EXAMPLES")
    print("="*70)
    
    # First, let's create a test job
    from insert_job import insert_job
    
    try:
        print("\n0. Creating test job...")
        job_id = insert_job(
            job_title="Python Developer",
            description="Looking for Python developer",
            required_skills="Python, Flask, MongoDB",
            experience="2-3 years",
            location="Remote"
        )
        print(f"   ✓ Test job created with ID: {job_id}")
    except Exception as e:
        print(f"   ⚠ Using existing job or error: {e}")
        # Use a sample job_id for testing
        job_id = "507f1f77bcf86cd799439011"
    
    try:
        # Example 1: Insert a candidate
        print("\n1. Inserting candidate...")
        candidate_id = insert_candidate(
            candidate_name="John Doe",
            email="john.doe@example.com",
            resume_file="uploads/20240115_john_resume.pdf",
            skills=["Python", "Flask", "MongoDB", "REST API"],
            job_id=job_id,
            phone="+1234567890",
            resume_text="Experienced Python developer with 5 years of experience...",
            experience="5 years"
        )
        print(f"   ✓ Candidate created with ID: {candidate_id}")
        
    except ValueError as e:
        print(f"   ✗ Validation error: {e}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    try:
        # Example 2: Save candidate on resume upload
        print("\n2. Saving candidate on resume upload...")
        candidate_id = save_candidate_on_resume_upload(
            candidate_name="Jane Smith",
            email="jane.smith@example.com",
            phone="+1234567891",
            resume_file="uploads/20240115_jane_resume.pdf",
            resume_text="Senior Python developer with expertise in Flask and MongoDB...",
            skills=["Python", "Flask", "MongoDB", "Docker", "AWS"],
            job_id=job_id,
            experience="7 years"
        )
        print(f"   ✓ Candidate saved with ID: {candidate_id}")
        
        # Update match score
        print("\n3. Updating match score...")
        success = update_candidate_match_score(candidate_id, 87.5)
        if success:
            print(f"   ✓ Match score updated to 87.5")
        
        # Update status
        print("\n4. Updating candidate status...")
        success = update_candidate_status(candidate_id, "shortlisted")
        if success:
            print(f"   ✓ Status updated to 'shortlisted'")
        
    except ValueError as e:
        print(f"   ✗ Validation error: {e}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Display all candidates
    print("\n" + "="*70)
    print("ALL CANDIDATES IN DATABASE")
    print("="*70)
    
    all_candidates = get_all_candidates()
    print(f"\nTotal candidates: {len(all_candidates)}\n")
    
    for candidate in all_candidates:
        print(f"ID: {candidate['_id']}")
        print(f"Name: {candidate['candidate_name']}")
        print(f"Email: {candidate['email']}")
        print(f"Skills: {', '.join(candidate['skills'])}")
        print(f"Job ID: {candidate['job_id']}")
        print(f"Match Score: {candidate.get('match_score', 0)}%")
        print(f"Status: {candidate['status']}")
        print(f"Created: {candidate['created_at']}")
        print("-" * 70)
    
    print()
