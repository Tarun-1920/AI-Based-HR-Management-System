# AI-Based HR Management System - Backend

A Flask-based REST API backend for an AI-powered HR Management System with resume matching capabilities.

## Features

- 🔐 **JWT Authentication** - Secure user authentication with role-based access
- 📄 **Resume Processing** - Extract text from PDF and DOCX files
- 🤖 **AI Resume Matching** - TF-IDF and cosine similarity for intelligent candidate ranking
- 💼 **Job Management** - Complete CRUD operations for job postings
- 👥 **Candidate Management** - Track and rank candidates with AI match scores
- 🗄️ **MongoDB Integration** - Scalable NoSQL database with optimized indexes
- ✅ **Comprehensive Validation** - Input validation and error handling
- 🌐 **CORS Enabled** - Ready for React frontend integration

## Tech Stack

- **Framework:** Flask 3.0
- **Database:** MongoDB with PyMongo
- **AI/ML:** scikit-learn (TF-IDF, Cosine Similarity)
- **NLP:** NLTK, spaCy
- **Document Processing:** PyPDF2, python-docx
- **Authentication:** JWT (PyJWT)
- **Security:** bcrypt for password hashing

## Project Structure

```
backend/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── database.py                 # MongoDB connection manager
├── utils.py                    # Validation and helper functions
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── .gitignore                  # Git ignore rules
│
├── routes/                     # API route handlers
│   ├── auth_routes.py         # Authentication endpoints
│   ├── job_routes.py          # Job management endpoints
│   ├── resume_routes.py       # Resume upload & parsing
│   └── candidate_routes.py    # Candidate management
│
├── models/                     # Database models
│   ├── user_model.py          # User model
│   ├── job_model.py           # Job model
│   └── candidate_model.py     # Candidate model
│
├── services/                   # Business logic layer
│   ├── job_service.py         # Job services
│   └── candidate_service.py   # Candidate services with AI
│
├── ai/                         # AI/ML modules
│   ├── resume_matcher.py      # TF-IDF matching algorithm
│   └── resume_parser.py       # Text extraction from resumes
│
└── uploads/                    # Resume file storage
```

## Installation

### Prerequisites

- Python 3.8+
- MongoDB 4.0+
- pip

### Setup

1. **Clone the repository**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file:
```env
MONGO_URI=mongodb://localhost:27017/ai_hr_system
DATABASE_NAME=ai_hr_system
SECRET_KEY=your-secret-key-change-in-production
JWT_EXPIRATION_HOURS=24
UPLOAD_FOLDER=uploads
DEBUG=True
HOST=0.0.0.0
PORT=5000
```

5. **Start MongoDB**
```bash
mongod
```

6. **Run the application**
```bash
python app.py
```

Server will start at `http://localhost:5000`

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login and get JWT token |
| GET | `/api/auth/verify` | Verify token validity |

### Jobs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/jobs` | Get all jobs |
| GET | `/api/jobs/:id` | Get single job |
| POST | `/api/jobs` | Create new job |
| PUT | `/api/jobs/:id` | Update job |
| DELETE | `/api/jobs/:id` | Delete job |
| GET | `/api/jobs/active` | Get active jobs only |

### Resumes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/resumes/upload-resume` | Upload resume file |
| POST | `/api/resumes/parse` | Parse resume and extract text |
| POST | `/api/resumes/match` | Calculate match score |
| POST | `/api/resumes/detailed-match` | Get detailed analysis |
| POST | `/api/resumes/extract-skills` | Extract skills from text |

### Candidates

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/candidates` | Get all ranked candidates |
| GET | `/api/candidates/:id` | Get single candidate |
| GET | `/api/candidates/job/:job_id` | Get candidates for job |
| POST | `/api/candidates` | Create candidate with AI matching |
| PUT | `/api/candidates/:id` | Update candidate |
| PUT | `/api/candidates/:id/status` | Update candidate status |
| DELETE | `/api/candidates/:id` | Delete candidate |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/api/health` | Health check |
| GET | `/api/stats` | Database statistics |

## API Examples

### Register User
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe",
  "role": "HR"
}
```

### Create Job
```bash
POST /api/jobs
Content-Type: application/json

{
  "job_title": "Senior Python Developer",
  "description": "We are looking for...",
  "required_skills": "Python, Flask, MongoDB",
  "experience": "3-5 years",
  "location": "Remote",
  "salary_range": "$80,000 - $120,000"
}
```

### Upload Resume
```bash
POST /api/resumes/upload-resume
Content-Type: multipart/form-data

candidate_name: John Doe
email: john@example.com
job_id: 65a1b2c3d4e5f6g7h8i9j0k1
resume: [file]
```

### Get Ranked Candidates
```bash
GET /api/candidates?job_id=65a1b2c3d4e5f6g7h8i9j0k1&sort_by_score=true
```

## Error Handling

All endpoints return standardized error responses:

```json
{
  "success": false,
  "error": "Error message here"
}
```

### HTTP Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict (duplicate)
- `413` - Payload Too Large
- `500` - Internal Server Error

## Testing

Run test scripts:

```bash
# Test database connection
python test_database.py

# Test resume parser
python test_resume_parser.py

# Test AI matcher
python test_resume_matcher.py

# Test candidates API
python test_candidates_api.py
```

## Database Collections

### users
- email (unique)
- password (hashed)
- name
- role (HR/Candidate/Admin)

### jobs
- job_title
- description
- required_skills
- experience
- location
- salary_range
- status (open/closed)
- created_at

### candidates
- name
- email
- phone
- resume_text
- skills
- experience
- job_id
- match_score (AI calculated)
- status (pending/shortlisted/interviewed/rejected/hired)
- applied_at

## Security Features

- ✅ Password hashing with bcrypt
- ✅ JWT token authentication
- ✅ Input validation and sanitization
- ✅ SQL injection prevention (NoSQL)
- ✅ File upload validation
- ✅ CORS configuration
- ✅ Environment variable protection

## AI Matching Algorithm

The system uses **TF-IDF (Term Frequency-Inverse Document Frequency)** and **Cosine Similarity** to match resumes with job descriptions:

1. **Text Preprocessing** - Lowercase, remove special characters
2. **TF-IDF Vectorization** - Convert text to numerical vectors
3. **Cosine Similarity** - Calculate angle between vectors
4. **Match Score** - Return percentage (0-100%)

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

MIT License

## Support

For issues and questions, please create an issue in the repository.
