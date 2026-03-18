"""
Test Script for GET /api/jobs Endpoint

Test all variations of the jobs retrieval API.
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def print_section(title):
    """Print formatted section header."""
    print("\n" + "="*70)
    print(title)
    print("="*70)

def test_get_all_jobs():
    """Test GET /api/jobs - Get all jobs."""
    print_section("TEST 1: Get All Jobs (GET /api/jobs)")
    
    try:
        response = requests.get(f"{BASE_URL}/jobs")
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Total Jobs: {data['data']['count']}")
            
            if data['data']['jobs']:
                print("\nFirst 3 Jobs:")
                for i, job in enumerate(data['data']['jobs'][:3], 1):
                    print(f"\n{i}. {job['job_title']}")
                    print(f"   ID: {job['_id']}")
                    print(f"   Location: {job['location']}")
                    print(f"   Status: {job['status']}")
                    print(f"   Experience: {job['experience']}")
        else:
            print(f"Error: {response.json()}")
        
    except Exception as e:
        print(f"Error: {e}")

def test_get_open_jobs():
    """Test GET /api/jobs?status=open - Get open jobs."""
    print_section("TEST 2: Get Open Jobs (GET /api/jobs?status=open)")
    
    try:
        response = requests.get(f"{BASE_URL}/jobs?status=open")
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Open Jobs: {data['data']['count']}")
            
            if data['data']['jobs']:
                print("\nOpen Positions:")
                for job in data['data']['jobs']:
                    print(f"  - {job['job_title']} ({job['location']})")
        
    except Exception as e:
        print(f"Error: {e}")

def test_get_remote_jobs():
    """Test GET /api/jobs?location=Remote - Get remote jobs."""
    print_section("TEST 3: Get Remote Jobs (GET /api/jobs?location=Remote)")
    
    try:
        response = requests.get(f"{BASE_URL}/jobs?location=Remote")
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Remote Jobs: {data['data']['count']}")
        
    except Exception as e:
        print(f"Error: {e}")

def test_search_jobs():
    """Test GET /api/jobs?search=Python - Search jobs."""
    print_section("TEST 4: Search Jobs (GET /api/jobs?search=Python)")
    
    try:
        response = requests.get(f"{BASE_URL}/jobs?search=Python")
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Python Jobs Found: {data['data']['count']}")
            
            if data['data']['jobs']:
                print("\nMatching Jobs:")
                for job in data['data']['jobs']:
                    print(f"  - {job['job_title']}")
        
    except Exception as e:
        print(f"Error: {e}")

def test_get_recent_jobs():
    """Test GET /api/jobs?recent=5 - Get recent jobs."""
    print_section("TEST 5: Get Recent Jobs (GET /api/jobs?recent=5)")
    
    try:
        response = requests.get(f"{BASE_URL}/jobs?recent=5")
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Recent Jobs: {data['data']['count']}")
        
    except Exception as e:
        print(f"Error: {e}")

def test_pagination():
    """Test GET /api/jobs?page=1&per_page=5 - Pagination."""
    print_section("TEST 6: Pagination (GET /api/jobs?page=1&per_page=5)")
    
    try:
        response = requests.get(f"{BASE_URL}/jobs?page=1&per_page=5")
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            
            if 'pagination' in data['data']:
                pagination = data['data']['pagination']
                print(f"\nPagination Info:")
                print(f"  Page: {pagination['page']}")
                print(f"  Per Page: {pagination['per_page']}")
                print(f"  Total: {pagination['total']}")
                print(f"  Total Pages: {pagination['total_pages']}")
                print(f"  Jobs on this page: {len(data['data']['jobs'])}")
        
    except Exception as e:
        print(f"Error: {e}")

def test_get_single_job():
    """Test GET /api/jobs/:id - Get single job."""
    print_section("TEST 7: Get Single Job (GET /api/jobs/:id)")
    
    # First get all jobs to get a valid ID
    try:
        response = requests.get(f"{BASE_URL}/jobs")
        if response.status_code == 200:
            data = response.json()
            if data['data']['jobs']:
                job_id = data['data']['jobs'][0]['_id']
                
                print(f"\nTesting with Job ID: {job_id}")
                
                # Get single job
                response = requests.get(f"{BASE_URL}/jobs/{job_id}")
                
                print(f"Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    job = data['data']['job']
                    print(f"\nJob Details:")
                    print(f"  Title: {job['job_title']}")
                    print(f"  Description: {job['description'][:100]}...")
                    print(f"  Location: {job['location']}")
                    print(f"  Experience: {job['experience']}")
                    print(f"  Skills: {job['required_skills']}")
                    print(f"  Status: {job['status']}")
            else:
                print("No jobs available to test")
        
    except Exception as e:
        print(f"Error: {e}")

def test_get_job_stats():
    """Test GET /api/jobs/stats - Get statistics."""
    print_section("TEST 8: Get Job Statistics (GET /api/jobs/stats)")
    
    try:
        response = requests.get(f"{BASE_URL}/jobs/stats")
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            stats = data['data']
            print(f"\nJob Statistics:")
            print(f"  Total Jobs: {stats['total_jobs']}")
            print(f"  Open Jobs: {stats['open_jobs']}")
            print(f"  Closed Jobs: {stats['closed_jobs']}")
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("GET /api/jobs ENDPOINT - TEST SUITE")
    print("="*70)
    print("\nMake sure Flask server is running on http://localhost:5000")
    
    input("\nPress Enter to start tests...")
    
    # Run all tests
    test_get_all_jobs()
    test_get_open_jobs()
    test_get_remote_jobs()
    test_search_jobs()
    test_get_recent_jobs()
    test_pagination()
    test_get_single_job()
    test_get_job_stats()
    
    print_section("TEST SUMMARY")
    print("\n✓ All tests completed")
    print("\nAPI Endpoints Tested:")
    print("  GET /api/jobs                    - Get all jobs")
    print("  GET /api/jobs?status=open        - Filter by status")
    print("  GET /api/jobs?location=Remote    - Filter by location")
    print("  GET /api/jobs?search=Python      - Search jobs")
    print("  GET /api/jobs?recent=5           - Get recent jobs")
    print("  GET /api/jobs?page=1&per_page=5  - Pagination")
    print("  GET /api/jobs/:id                - Get single job")
    print("  GET /api/jobs/stats              - Get statistics")
    
    print("\n📝 Example cURL Commands:")
    print("\n# Get all jobs")
    print("curl http://localhost:5000/api/jobs")
    print("\n# Get open jobs")
    print("curl http://localhost:5000/api/jobs?status=open")
    print("\n# Search for Python jobs")
    print("curl http://localhost:5000/api/jobs?search=Python")
    print()

if __name__ == "__main__":
    main()
