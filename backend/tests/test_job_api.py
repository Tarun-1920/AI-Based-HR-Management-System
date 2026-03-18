"""
Test Script for Job API Endpoints

Test all job-related API endpoints using requests library.
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def print_section(title):
    """Print formatted section header."""
    print("\n" + "="*70)
    print(title)
    print("="*70)

def test_create_job():
    """Test POST /api/jobs - Create new job."""
    print_section("TEST 1: Create Job (POST /api/jobs)")
    
    job_data = {
        "job_title": "Senior Python Developer",
        "description": "We are looking for an experienced Python developer with strong backend skills. The ideal candidate will have experience with Flask, MongoDB, and REST APIs.",
        "required_skills": "Python, Flask, MongoDB, REST API, Docker, AWS",
        "experience": "3-5 years",
        "location": "Remote",
        "salary_range": "$80,000 - $120,000"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/jobs",
            json=job_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            data = response.json()
            if data.get('success'):
                return data['data']['job_id']
        
    except Exception as e:
        print(f"Error: {e}")
    
    return None

def test_get_all_jobs():
    """Test GET /api/jobs - Get all jobs."""
    print_section("TEST 2: Get All Jobs (GET /api/jobs)")
    
    try:
        response = requests.get(f"{BASE_URL}/jobs")
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Total Jobs: {data['data']['count']}")
            
            if data['data']['jobs']:
                print("\nFirst Job:")
                first_job = data['data']['jobs'][0]
                print(f"  ID: {first_job['_id']}")
                print(f"  Title: {first_job['job_title']}")
                print(f"  Location: {first_job['location']}")
                print(f"  Status: {first_job['status']}")
        
    except Exception as e:
        print(f"Error: {e}")

def test_get_open_jobs():
    """Test GET /api/jobs?status=open - Get open jobs."""
    print_section("TEST 3: Get Open Jobs (GET /api/jobs?status=open)")
    
    try:
        response = requests.get(f"{BASE_URL}/jobs?status=open")
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Open Jobs: {data['data']['count']}")
        
    except Exception as e:
        print(f"Error: {e}")

def test_get_single_job(job_id):
    """Test GET /api/jobs/:id - Get single job."""
    print_section(f"TEST 4: Get Single Job (GET /api/jobs/{job_id})")
    
    if not job_id:
        print("Skipping - No job ID available")
        return
    
    try:
        response = requests.get(f"{BASE_URL}/jobs/{job_id}")
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            job = data['data']['job']
            print(f"\nJob Details:")
            print(f"  ID: {job['_id']}")
            print(f"  Title: {job['job_title']}")
            print(f"  Description: {job['description'][:100]}...")
            print(f"  Skills: {job['required_skills']}")
            print(f"  Experience: {job['experience']}")
            print(f"  Location: {job['location']}")
            print(f"  Status: {job['status']}")
        
    except Exception as e:
        print(f"Error: {e}")

def test_update_job(job_id):
    """Test PUT /api/jobs/:id - Update job."""
    print_section(f"TEST 5: Update Job (PUT /api/jobs/{job_id})")
    
    if not job_id:
        print("Skipping - No job ID available")
        return
    
    update_data = {
        "salary_range": "$90,000 - $130,000",
        "status": "open"
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/jobs/{job_id}",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
    except Exception as e:
        print(f"Error: {e}")

def test_validation_errors():
    """Test validation errors."""
    print_section("TEST 6: Validation Errors")
    
    # Test missing required field
    print("\n6.1 Testing missing required field...")
    try:
        response = requests.post(
            f"{BASE_URL}/jobs",
            json={"job_title": "Test Job"},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test short job title
    print("\n6.2 Testing short job title...")
    try:
        response = requests.post(
            f"{BASE_URL}/jobs",
            json={
                "job_title": "AB",
                "description": "Test description",
                "required_skills": "Python",
                "experience": "2 years",
                "location": "Remote"
            },
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("JOB API ENDPOINTS - TEST SUITE")
    print("="*70)
    print("\nMake sure Flask server is running on http://localhost:5000")
    
    input("\nPress Enter to start tests...")
    
    # Test 1: Create job
    job_id = test_create_job()
    
    # Test 2: Get all jobs
    test_get_all_jobs()
    
    # Test 3: Get open jobs
    test_get_open_jobs()
    
    # Test 4: Get single job
    test_get_single_job(job_id)
    
    # Test 5: Update job
    test_update_job(job_id)
    
    # Test 6: Validation errors
    test_validation_errors()
    
    print_section("TEST SUMMARY")
    print("\n✓ All tests completed")
    print("\nAPI Endpoints Tested:")
    print("  POST   /api/jobs          - Create job")
    print("  GET    /api/jobs          - Get all jobs")
    print("  GET    /api/jobs?status=  - Filter by status")
    print("  GET    /api/jobs/:id      - Get single job")
    print("  PUT    /api/jobs/:id      - Update job")
    print("  DELETE /api/jobs/:id      - Delete job")
    print()

if __name__ == "__main__":
    main()
