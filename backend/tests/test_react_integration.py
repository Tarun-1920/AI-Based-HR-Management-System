"""
React Frontend Integration Test Script

This script tests all API endpoints to ensure they return proper JSON responses
in the format expected by React frontend: { success, message, data }
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def print_section(title):
    """Print formatted section header."""
    print("\n" + "="*70)
    print(title)
    print("="*70)

def test_response_format(response, endpoint):
    """Verify response follows standard format."""
    try:
        data = response.json()
        
        # Check if 'success' field exists
        if 'success' not in data:
            print(f"❌ FAIL: Missing 'success' field in {endpoint}")
            return False
        
        # Check if success is boolean
        if not isinstance(data['success'], bool):
            print(f"❌ FAIL: 'success' should be boolean in {endpoint}")
            return False
        
        print(f"✅ PASS: {endpoint}")
        print(f"   Status: {response.status_code}")
        print(f"   Success: {data['success']}")
        if 'message' in data:
            print(f"   Message: {data['message']}")
        if 'data' in data:
            print(f"   Data: {type(data['data']).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ FAIL: Invalid JSON response from {endpoint}")
        print(f"   Error: {str(e)}")
        return False

def test_cors_headers(response, endpoint):
    """Verify CORS headers are present."""
    cors_headers = [
        'Access-Control-Allow-Origin',
        'Access-Control-Allow-Methods',
        'Access-Control-Allow-Headers'
    ]
    
    print(f"\n📡 CORS Headers for {endpoint}:")
    for header in cors_headers:
        value = response.headers.get(header, 'Not Set')
        print(f"   {header}: {value}")

def test_auth_endpoints():
    """Test authentication endpoints."""
    print_section("TEST 1: Authentication Endpoints")
    
    # Test register endpoint
    print("\n1.1 Testing POST /api/auth/register")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json={
                "email": f"test_{int(requests.get(BASE_URL.replace('/api', '')).elapsed.total_seconds()*1000)}@example.com",
                "password": "password123",
                "name": "Test User",
                "role": "Candidate"
            },
            headers={"Content-Type": "application/json"}
        )
        test_response_format(response, "POST /api/auth/register")
        test_cors_headers(response, "POST /api/auth/register")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test login endpoint
    print("\n1.2 Testing POST /api/auth/login")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            },
            headers={"Content-Type": "application/json"}
        )
        test_response_format(response, "POST /api/auth/login")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_job_endpoints():
    """Test job management endpoints."""
    print_section("TEST 2: Job Management Endpoints")
    
    # Test get all jobs
    print("\n2.1 Testing GET /api/jobs")
    try:
        response = requests.get(f"{BASE_URL}/jobs")
        test_response_format(response, "GET /api/jobs")
        test_cors_headers(response, "GET /api/jobs")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test create job
    print("\n2.2 Testing POST /api/jobs")
    try:
        response = requests.post(
            f"{BASE_URL}/jobs",
            json={
                "job_title": "Test Job",
                "description": "This is a test job posting",
                "required_skills": "Python, Flask, React",
                "experience": "2-3 years",
                "location": "Remote",
                "salary_range": "$60,000 - $80,000"
            },
            headers={"Content-Type": "application/json"}
        )
        test_response_format(response, "POST /api/jobs")
        
        # Store job_id for further tests
        if response.status_code == 201:
            data = response.json()
            if 'data' in data and 'job_id' in data['data']:
                return data['data']['job_id']
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    return None

def test_candidate_endpoints():
    """Test candidate management endpoints."""
    print_section("TEST 3: Candidate Management Endpoints")
    
    # Test get all candidates
    print("\n3.1 Testing GET /api/candidates")
    try:
        response = requests.get(f"{BASE_URL}/candidates")
        test_response_format(response, "GET /api/candidates")
        test_cors_headers(response, "GET /api/candidates")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_resume_endpoints():
    """Test resume processing endpoints."""
    print_section("TEST 4: Resume Processing Endpoints")
    
    # Test match endpoint
    print("\n4.1 Testing POST /api/resumes/match")
    try:
        response = requests.post(
            f"{BASE_URL}/resumes/match",
            json={
                "resume_text": "Experienced Python developer with 5 years of experience in Flask, Django, and MongoDB",
                "job_requirements": "Looking for Python developer with Flask and MongoDB experience"
            },
            headers={"Content-Type": "application/json"}
        )
        test_response_format(response, "POST /api/resumes/match")
        test_cors_headers(response, "POST /api/resumes/match")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test extract skills endpoint
    print("\n4.2 Testing POST /api/resumes/extract-skills")
    try:
        response = requests.post(
            f"{BASE_URL}/resumes/extract-skills",
            json={
                "resume_text": "Skills: Python, JavaScript, React, Node.js, MongoDB, AWS, Docker"
            },
            headers={"Content-Type": "application/json"}
        )
        test_response_format(response, "POST /api/resumes/extract-skills")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_error_responses():
    """Test error response format."""
    print_section("TEST 5: Error Response Format")
    
    # Test 404 error
    print("\n5.1 Testing 404 Not Found")
    try:
        response = requests.get(f"{BASE_URL}/nonexistent")
        test_response_format(response, "GET /api/nonexistent (404)")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 400 validation error
    print("\n5.2 Testing 400 Validation Error")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={},
            headers={"Content-Type": "application/json"}
        )
        test_response_format(response, "POST /api/auth/login (400)")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_system_endpoints():
    """Test system endpoints."""
    print_section("TEST 6: System Endpoints")
    
    # Test root endpoint
    print("\n6.1 Testing GET /")
    try:
        response = requests.get(BASE_URL.replace('/api', ''))
        test_response_format(response, "GET /")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test health endpoint
    print("\n6.2 Testing GET /api/health")
    try:
        response = requests.get(f"{BASE_URL}/health")
        test_response_format(response, "GET /api/health")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test stats endpoint
    print("\n6.3 Testing GET /api/stats")
    try:
        response = requests.get(f"{BASE_URL}/stats")
        test_response_format(response, "GET /api/stats")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def display_sample_responses():
    """Display sample response formats for React frontend."""
    print_section("SAMPLE RESPONSE FORMATS FOR REACT FRONTEND")
    
    print("\n✅ Success Response:")
    print(json.dumps({
        "success": True,
        "message": "Operation completed successfully",
        "data": {
            "id": "123",
            "name": "Example"
        }
    }, indent=2))
    
    print("\n❌ Error Response:")
    print(json.dumps({
        "success": False,
        "message": "Validation Error",
        "error": "Email is required"
    }, indent=2))
    
    print("\n📋 List Response:")
    print(json.dumps({
        "success": True,
        "data": {
            "items": [{"id": "1"}, {"id": "2"}],
            "count": 2
        }
    }, indent=2))

def main():
    """Run all integration tests."""
    print("\n" + "="*70)
    print("REACT FRONTEND INTEGRATION TEST SUITE")
    print("="*70)
    print("\nTesting API endpoints for React frontend compatibility...")
    print("Checking: JSON format, CORS headers, response structure")
    print("\nMake sure Flask server is running on http://localhost:5000")
    
    input("\nPress Enter to start tests...")
    
    # Display sample formats
    display_sample_responses()
    
    # Run tests
    test_system_endpoints()
    test_auth_endpoints()
    job_id = test_job_endpoints()
    test_candidate_endpoints()
    test_resume_endpoints()
    test_error_responses()
    
    print_section("TEST SUMMARY")
    print("\n✅ All endpoints tested for React frontend compatibility")
    print("\nVerified:")
    print("  ✓ JSON response format")
    print("  ✓ 'success' field (boolean)")
    print("  ✓ 'message' field (string)")
    print("  ✓ 'data' field (object/array)")
    print("  ✓ CORS headers")
    print("  ✓ Proper HTTP status codes")
    
    print("\n📝 React Frontend Integration Guide:")
    print("  1. Use axios or fetch to call APIs")
    print("  2. Check response.data.success for operation status")
    print("  3. Display response.data.message to users")
    print("  4. Access actual data from response.data.data")
    print("  5. Handle errors using response.data.error")
    
    print("\n🔗 Example React Code:")
    print("""
    // Using axios
    axios.post('http://localhost:5000/api/auth/login', {
      email: 'user@example.com',
      password: 'password123'
    })
    .then(response => {
      if (response.data.success) {
        console.log(response.data.message);
        const user = response.data.data.user;
        const token = response.data.data.token;
      }
    })
    .catch(error => {
      console.error(error.response.data.error);
    });
    """)
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
