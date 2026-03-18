"""
Test script for Ranked Candidates API.

This script demonstrates how the GET /api/candidates endpoint
retrieves, ranks, and returns candidates based on AI match scores.
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def print_section(title):
    """Print formatted section header."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

def test_get_all_candidates():
    """Test GET /api/candidates - Get all ranked candidates."""
    print_section("TEST 1: Get All Ranked Candidates")
    
    try:
        response = requests.get(f"{BASE_URL}/candidates")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Success! Found {data['count']} candidates")
            print()
            
            # Display top 5 candidates
            for i, candidate in enumerate(data['candidates'][:5], 1):
                print(f"{i}. {candidate['candidate_name']}")
                print(f"   Email: {candidate['email']}")
                print(f"   Job Applied: {candidate['job_applied']}")
                print(f"   Match Score: {candidate['match_score']}%")
                print(f"   Skills: {', '.join(candidate['skills'][:5])}")
                print(f"   Status: {candidate['status']}")
                print()
        else:
            print(f"✗ Error: {response.status_code}")
            print(response.json())
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")

def test_get_candidates_by_job():
    """Test GET /api/candidates/job/:job_id - Get ranked candidates for specific job."""
    print_section("TEST 2: Get Ranked Candidates for Specific Job")
    
    job_id = input("Enter Job ID (or press Enter to skip): ").strip()
    
    if not job_id:
        print("Skipped")
        return
    
    try:
        response = requests.get(f"{BASE_URL}/candidates/job/{job_id}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Success! Job: {data['job_title']}")
            print(f"Found {data['count']} candidates")
            print()
            
            for i, candidate in enumerate(data['candidates'], 1):
                print(f"{i}. {candidate['candidate_name']} - {candidate['match_score']}%")
                print(f"   Email: {candidate['email']}")
                print(f"   Status: {candidate['status']}")
                print()
        else:
            print(f"✗ Error: {response.status_code}")
            print(response.json())
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")

def test_get_candidates_with_filter():
    """Test GET /api/candidates?job_id=xxx - Filter candidates by job."""
    print_section("TEST 3: Get Candidates with Query Parameters")
    
    job_id = input("Enter Job ID to filter (or press Enter to skip): ").strip()
    
    if not job_id:
        print("Skipped")
        return
    
    try:
        response = requests.get(f"{BASE_URL}/candidates?job_id={job_id}&sort_by_score=true")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Success! Found {data['count']} candidates for this job")
            print()
            
            for i, candidate in enumerate(data['candidates'], 1):
                print(f"Rank {i}: {candidate['candidate_name']} - {candidate['match_score']}%")
                
        else:
            print(f"✗ Error: {response.status_code}")
            print(response.json())
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")

def test_create_candidate():
    """Test POST /api/candidates - Create new candidate with AI matching."""
    print_section("TEST 4: Create New Candidate (with AI Matching)")
    
    print("This will create a test candidate and calculate match score automatically.")
    proceed = input("Proceed? (y/n): ").strip().lower()
    
    if proceed != 'y':
        print("Skipped")
        return
    
    job_id = input("Enter Job ID: ").strip()
    
    if not job_id:
        print("Job ID required. Skipped.")
        return
    
    candidate_data = {
        "name": "Test Candidate",
        "email": "test@example.com",
        "phone": "+1234567890",
        "resume_text": """
        Experienced Python Developer with 5 years of experience.
        Skills: Python, Flask, Django, MongoDB, PostgreSQL, AWS, Docker, Kubernetes
        Experience with REST API development and microservices architecture.
        Strong knowledge of machine learning and data analysis.
        """,
        "skills": ["Python", "Flask", "MongoDB", "AWS", "Docker"],
        "experience": "5 years",
        "job_id": job_id
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/candidates",
            json=candidate_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"✓ Success! {data['message']}")
            print(f"Candidate ID: {data['candidate_id']}")
            print("Match score calculated automatically!")
        else:
            print(f"✗ Error: {response.status_code}")
            print(response.json())
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")

def display_sample_response():
    """Display sample API response format."""
    print_section("SAMPLE API RESPONSE FORMAT")
    
    sample_response = {
        "success": True,
        "count": 3,
        "candidates": [
            {
                "candidate_id": "65a1b2c3d4e5f6g7h8i9j0k1",
                "candidate_name": "John Doe",
                "email": "john@example.com",
                "phone": "+1234567890",
                "job_applied": "Senior Python Developer",
                "job_id": "65a1b2c3d4e5f6g7h8i9j0k2",
                "skills": ["Python", "Flask", "MongoDB", "AWS", "Docker"],
                "experience": "5 years",
                "match_score": 87.45,
                "status": "shortlisted",
                "applied_at": "2024-01-15T10:30:00"
            },
            {
                "candidate_id": "65a1b2c3d4e5f6g7h8i9j0k3",
                "candidate_name": "Jane Smith",
                "email": "jane@example.com",
                "phone": "+1234567891",
                "job_applied": "Senior Python Developer",
                "job_id": "65a1b2c3d4e5f6g7h8i9j0k2",
                "skills": ["Python", "Django", "PostgreSQL"],
                "experience": "3 years",
                "match_score": 72.30,
                "status": "pending",
                "applied_at": "2024-01-15T11:00:00"
            }
        ]
    }
    
    print(json.dumps(sample_response, indent=2))

def main():
    """Main test runner."""
    print("\n" + "=" * 70)
    print("RANKED CANDIDATES API - TEST SUITE")
    print("=" * 70)
    print("\nMake sure the Flask server is running on http://localhost:5000")
    print()
    
    # Display sample response format
    display_sample_response()
    
    # Run tests
    test_get_all_candidates()
    test_get_candidates_by_job()
    test_get_candidates_with_filter()
    test_create_candidate()
    
    print_section("TESTS COMPLETED")
    print("\nAPI Endpoints Available:")
    print("  GET  /api/candidates")
    print("  GET  /api/candidates?job_id=xxx")
    print("  GET  /api/candidates/job/:job_id")
    print("  GET  /api/candidates/:candidate_id")
    print("  POST /api/candidates")
    print("  PUT  /api/candidates/:candidate_id")
    print("  PUT  /api/candidates/:candidate_id/status")
    print("  DELETE /api/candidates/:candidate_id")
    print()

if __name__ == "__main__":
    main()
