# Backend Integration Guide - AI HR Management System

## Current Status

### Frontend Status: ✅ READY
- ✅ All UI components built
- ✅ All pages implemented
- ✅ API service layer configured
- ✅ Error handling implemented
- ✅ Loading states added
- ✅ Toast notifications ready
- ✅ Responsive design complete
- ✅ Production optimized

### Backend Status: ❌ NOT CONNECTED
- ❌ No backend server running
- ❌ No database connected
- ❌ No API endpoints implemented
- ❌ No AI services integrated
- ❌ No authentication system

## Frontend API Configuration

### Current API Base URL
```javascript
// src/utils/api.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
```

### Environment Variables
Create `.env` file in frontend root:
```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENV=development
```

For production:
```
REACT_APP_API_URL=https://api.yourdomain.com/api
REACT_APP_ENV=production
```

## Required Backend API Endpoints

### 1. Authentication Endpoints

#### POST `/api/login`
**Request**:
```json
{
  "email": "user@example.com",
  "password": "password123",
  "role": "hr" | "candidate"
}
```

**Response**:
```json
{
  "token": "jwt_token_here",
  "name": "John Doe",
  "role": "hr",
  "id": "user_id"
}
```

**Status Codes**:
- 200: Success
- 401: Invalid credentials
- 400: Missing fields

---

### 2. Jobs Endpoints

#### GET `/api/jobs`
**Query Parameters**:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)
- `status`: Job status filter

**Response**:
```json
{
  "jobs": [
    {
      "id": "job_id",
      "title": "Senior Python Developer",
      "company": "TechCorp Inc.",
      "description": "Job description",
      "skills": ["Python", "Django", "PostgreSQL"],
      "experience": "3-5 years",
      "salary": "$80,000 - $120,000",
      "location": "New York, NY",
      "createdAt": "2024-01-15T10:00:00Z",
      "status": "active"
    }
  ],
  "total": 24,
  "page": 1
}
```

#### POST `/api/jobs`
**Headers**: `Authorization: Bearer {token}`

**Request**:
```json
{
  "title": "Senior Python Developer",
  "company": "TechCorp Inc.",
  "description": "Job description",
  "skills": ["Python", "Django", "PostgreSQL"],
  "experience": "3-5 years",
  "salary": "$80,000 - $120,000",
  "location": "New York, NY"
}
```

**Response**:
```json
{
  "id": "job_id",
  "title": "Senior Python Developer",
  "message": "Job posted successfully"
}
```

#### PUT `/api/jobs/{jobId}`
**Headers**: `Authorization: Bearer {token}`

**Request**: Same as POST

**Response**: Updated job object

#### DELETE `/api/jobs/{jobId}`
**Headers**: `Authorization: Bearer {token}`

**Response**:
```json
{
  "message": "Job deleted successfully"
}
```

---

### 3. Candidates Endpoints

#### GET `/api/candidates`
**Query Parameters**:
- `page`: Page number
- `limit`: Items per page
- `jobId`: Filter by job
- `status`: Filter by status (new, reviewed, shortlisted, interviewed, rejected)
- `search`: Search by name or skills

**Response**:
```json
{
  "candidates": [
    {
      "id": "candidate_id",
      "firstName": "Alice",
      "lastName": "Johnson",
      "email": "alice@example.com",
      "phone": "+1 (555) 123-4567",
      "jobId": "job_id",
      "jobTitle": "Senior Python Developer",
      "matchScore": 94,
      "experience": "4 years",
      "location": "New York, NY",
      "skills": ["Python", "Django", "PostgreSQL"],
      "education": "BS Computer Science",
      "status": "new",
      "appliedDate": "2024-01-15T10:00:00Z",
      "resumeUrl": "/resumes/alice_johnson.pdf"
    }
  ],
  "total": 156,
  "page": 1
}
```

#### POST `/api/upload-resume`
**Headers**: 
- `Authorization: Bearer {token}`
- `Content-Type: multipart/form-data`

**Form Data**:
```
firstName: "Alice"
lastName: "Johnson"
email: "alice@example.com"
phone: "+1 (555) 123-4567"
experience: "4 years"
expectedSalary: "$80,000 - $100,000"
location: "New York, NY"
jobId: "job_id"
resume: <file>
```

**Response**:
```json
{
  "id": "candidate_id",
  "message": "Resume uploaded successfully",
  "matchScore": 94,
  "analysis": {
    "skills": ["Python", "Django", "PostgreSQL"],
    "experience": "4 years",
    "education": "BS Computer Science"
  }
}
```

#### GET `/api/candidates/{candidateId}`
**Headers**: `Authorization: Bearer {token}`

**Response**: Single candidate object

#### PATCH `/api/candidates/{candidateId}/status`
**Headers**: `Authorization: Bearer {token}`

**Request**:
```json
{
  "status": "shortlisted" | "interviewed" | "rejected" | "reviewed"
}
```

**Response**:
```json
{
  "id": "candidate_id",
  "status": "shortlisted",
  "message": "Status updated successfully"
}
```

#### GET `/api/candidates/job/{jobId}`
**Headers**: `Authorization: Bearer {token}`

**Response**: Array of candidates for specific job

#### GET `/api/candidates/{candidateId}/resume`
**Headers**: `Authorization: Bearer {token}`

**Response**: Resume file (PDF/DOCX)

---

### 4. AI Endpoints

#### POST `/api/ai/analyze-resume`
**Headers**: `Authorization: Bearer {token}`

**Request**:
```json
{
  "resumeText": "Resume content",
  "jobId": "job_id"
}
```

**Response**:
```json
{
  "skills": ["Python", "Django", "PostgreSQL"],
  "experience": "4 years",
  "education": "BS Computer Science",
  "matchScore": 94,
  "strengths": ["Strong Python skills", "Good database experience"],
  "gaps": ["Limited DevOps experience"]
}
```

#### POST `/api/ai/match-candidates/{jobId}`
**Headers**: `Authorization: Bearer {token}`

**Response**:
```json
{
  "matches": [
    {
      "candidateId": "candidate_id",
      "name": "Alice Johnson",
      "matchScore": 94,
      "matchReasons": ["Strong Python skills", "Relevant experience"]
    }
  ]
}
```

#### GET `/api/ai/match-score/{candidateId}/{jobId}`
**Headers**: `Authorization: Bearer {token}`

**Response**:
```json
{
  "candidateId": "candidate_id",
  "jobId": "job_id",
  "matchScore": 94,
  "analysis": {
    "skillsMatch": 95,
    "experienceMatch": 92,
    "educationMatch": 90
  }
}
```

---

### 5. Dashboard Endpoints

#### GET `/api/dashboard/stats`
**Headers**: `Authorization: Bearer {token}`

**Response**:
```json
{
  "totalJobs": 24,
  "totalApplicants": 156,
  "topCandidateMatch": 94,
  "aiProcessingStatus": "Active"
}
```

#### GET `/api/dashboard/activities`
**Headers**: `Authorization: Bearer {token}`

**Response**:
```json
{
  "activities": [
    {
      "id": "activity_id",
      "action": "New candidate applied for Senior Python Developer",
      "time": "2 minutes ago",
      "type": "application",
      "user": "Sarah Johnson"
    }
  ]
}
```

#### GET `/api/dashboard/top-candidates`
**Headers**: `Authorization: Bearer {token}`

**Response**:
```json
{
  "candidates": [
    {
      "id": "candidate_id",
      "name": "Alice Johnson",
      "position": "Senior Python Developer",
      "match": 94,
      "skills": ["Python", "Django", "PostgreSQL"],
      "status": "new"
    }
  ]
}
```

---

## Backend Technology Stack Recommendations

### Framework Options
1. **Node.js + Express** (Recommended)
   - Fast and lightweight
   - JavaScript ecosystem
   - Easy to integrate with frontend

2. **Python + Flask/Django**
   - Great for AI/ML integration
   - Extensive libraries
   - Good for data processing

3. **Python + FastAPI**
   - Modern and fast
   - Built-in async support
   - Great for AI services

### Database
- **PostgreSQL** (Recommended)
  - Robust and reliable
  - Good for complex queries
  - Excellent for production

- **MongoDB**
  - Flexible schema
  - Good for rapid development
  - Document-based

### AI/ML Services
- **OpenAI API** - For resume analysis
- **Hugging Face** - For NLP tasks
- **spaCy** - For text processing
- **scikit-learn** - For ML models

### Authentication
- **JWT (JSON Web Tokens)**
- **bcrypt** - For password hashing
- **OAuth 2.0** - For third-party integration

---

## Setup Instructions for Backend

### 1. Create Backend Project Structure
```bash
mkdir backend
cd backend
npm init -y
npm install express cors dotenv axios multer bcryptjs jsonwebtoken
```

### 2. Create Environment File
```bash
# .env
PORT=5000
DATABASE_URL=postgresql://user:password@localhost:5432/hr_system
JWT_SECRET=your_jwt_secret_key
OPENAI_API_KEY=your_openai_key
NODE_ENV=development
```

### 3. Enable CORS
```javascript
// server.js
const cors = require('cors');
app.use(cors({
  origin: 'http://localhost:3000',
  credentials: true
}));
```

### 4. Implement Authentication
```javascript
// middleware/auth.js
const jwt = require('jsonwebtoken');

const authMiddleware = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ message: 'No token' });
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ message: 'Invalid token' });
  }
};

module.exports = authMiddleware;
```

### 5. Implement API Endpoints
```javascript
// routes/jobs.js
const express = require('express');
const router = express.Router();
const authMiddleware = require('../middleware/auth');

router.get('/', async (req, res) => {
  // Get all jobs
});

router.post('/', authMiddleware, async (req, res) => {
  // Create job
});

module.exports = router;
```

---

## Testing the Integration

### 1. Test Login
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123","role":"hr"}'
```

### 2. Test Get Jobs
```bash
curl -X GET http://localhost:5000/api/jobs \
  -H "Authorization: Bearer {token}"
```

### 3. Test Resume Upload
```bash
curl -X POST http://localhost:5000/api/upload-resume \
  -H "Authorization: Bearer {token}" \
  -F "firstName=Alice" \
  -F "lastName=Johnson" \
  -F "email=alice@example.com" \
  -F "resume=@resume.pdf"
```

---

## Frontend-Backend Communication Flow

### Login Flow
```
Frontend (Login.js)
  ↓
User enters credentials
  ↓
POST /api/login
  ↓
Backend validates credentials
  ↓
Returns JWT token
  ↓
Frontend stores token in localStorage
  ↓
Redirect to Dashboard
```

### Resume Upload Flow
```
Frontend (UploadResume.js)
  ↓
User selects resume file
  ↓
POST /api/upload-resume (multipart/form-data)
  ↓
Backend processes resume
  ↓
AI analyzes resume
  ↓
Returns match score & analysis
  ↓
Frontend shows success notification
  ↓
Redirect to Dashboard
```

### Candidate Ranking Flow
```
Frontend (CandidateRanking.js)
  ↓
GET /api/candidates
  ↓
Backend queries database
  ↓
Returns candidates with match scores
  ↓
Frontend displays in table
  ↓
User can filter/sort
  ↓
PATCH /api/candidates/{id}/status
  ↓
Backend updates status
```

---

## Error Handling

### Frontend Error Handling
```javascript
try {
  const response = await authAPI.login(email, password, role);
  // Success
} catch (error) {
  const errorMsg = handleApiError(error);
  error('Login Failed', errorMsg);
}
```

### Backend Error Responses
```javascript
// 400 - Bad Request
{ "message": "Missing required fields" }

// 401 - Unauthorized
{ "message": "Invalid credentials" }

// 403 - Forbidden
{ "message": "Access denied" }

// 404 - Not Found
{ "message": "Resource not found" }

// 500 - Server Error
{ "message": "Internal server error" }
```

---

## Security Considerations

### Frontend
- ✅ JWT tokens stored in localStorage
- ✅ Automatic token injection in headers
- ✅ Auto-logout on 401 errors
- ✅ Input validation

### Backend
- ✅ Password hashing with bcrypt
- ✅ JWT token verification
- ✅ CORS configuration
- ✅ Rate limiting
- ✅ Input sanitization
- ✅ SQL injection prevention

---

## Deployment Checklist

### Frontend
- [ ] Build project: `npm run build`
- [ ] Set production API URL
- [ ] Test all features
- [ ] Deploy to hosting (Vercel, Netlify, AWS)

### Backend
- [ ] Set up database
- [ ] Configure environment variables
- [ ] Implement all endpoints
- [ ] Add error handling
- [ ] Add logging
- [ ] Deploy to server (Heroku, AWS, DigitalOcean)

---

## Next Steps

1. **Create Backend Project**
   - Set up Node.js/Express or Python/FastAPI
   - Configure database
   - Implement authentication

2. **Implement API Endpoints**
   - Follow the specifications above
   - Add error handling
   - Add logging

3. **Integrate AI Services**
   - Set up OpenAI API
   - Implement resume analysis
   - Implement candidate matching

4. **Test Integration**
   - Test each endpoint
   - Test frontend-backend communication
   - Test error scenarios

5. **Deploy**
   - Deploy backend
   - Update frontend API URL
   - Deploy frontend
   - Test in production

---

## Support Resources

- **Frontend API Service**: `src/utils/api.js`
- **API Error Handling**: `src/utils/api.js` (handleApiError function)
- **Component Documentation**: See individual component files
- **UI Integration Guide**: `UI_INTEGRATION_GUIDE.md`

---

## Summary

**Current Status**:
- ✅ Frontend: Fully built and ready
- ❌ Backend: Not implemented

**What's Needed**:
1. Backend server (Node.js/Python)
2. Database (PostgreSQL/MongoDB)
3. API endpoints (as specified above)
4. AI integration (OpenAI/Hugging Face)
5. Authentication system (JWT)

**Timeline**:
- Backend setup: 1-2 days
- API implementation: 3-5 days
- AI integration: 2-3 days
- Testing & deployment: 2-3 days

**Total**: 1-2 weeks for full integration

The frontend is production-ready and waiting for backend connection!
