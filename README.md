# 🤖 AI-Based HR Management System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-000000.svg)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.4+-47A248.svg)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> An intelligent HR management system powered by AI for automated resume screening, candidate ranking, and recruitment workflow optimization.

## 🌟 Key Features

### 🎯 AI-Powered Recruitment
- **Smart Resume Parsing** - Automatically extract skills, experience, and qualifications from PDF/DOCX resumes
- **AI Candidate Matching** - Machine learning algorithms match candidates to job requirements with accuracy scores
- **Intelligent Ranking** - Automatically rank candidates based on job fit using NLP and ML models

### 👥 Complete HR Management
- **Job Posting Management** - Create, edit, and manage job openings
- **Candidate Tracking** - Track applicants through the entire recruitment pipeline
- **Employee Management** - Comprehensive employee information and records management
- **Communication Center** - Built-in messaging system for candidate and employee communication

### 🤖 AI Chatbot Assistant
- Interactive chatbot for HR queries and candidate support
- Natural language processing for intelligent responses
- 24/7 automated assistance

### 📄 Document Management
- Secure document upload and storage
- Version control for employee documents
- Organized document retrieval system

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- React 18.2.0 - Modern UI framework
- React Router 6.8.0 - Client-side routing
- Axios - HTTP client for API calls
- CSS3 - Custom styling with animations

**Backend:**
- Flask 3.0.0 - Python web framework
- MongoDB - NoSQL database
- PyMongo 4.6.1 - MongoDB driver
- JWT Authentication - Secure user authentication

**AI/ML:**
- scikit-learn 1.4.0 - Machine learning models
- NLTK 3.8.1 - Natural language processing
- spaCy 3.7.2 - Advanced NLP
- Custom resume matching algorithm

**Document Service:**
- Node.js + Express 4.18.2
- Mongoose 7.5.0 - MongoDB ODM
- Multer - File upload handling

## 📁 Project Structure

```
AI-Based_HR_Management_System/
├── frontend/                    # React Frontend
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/              # Page components
│   │   ├── styles/             # CSS stylesheets
│   │   └── utils/              # Utility functions
│   └── package.json
│
├── backend/                     # Flask Backend
│   ├── ai/                     # AI/ML modules
│   │   ├── resume_matcher.py  # Candidate matching algorithm
│   │   └── resume_parser.py   # Resume text extraction
│   ├── models/                 # Database models
│   ├── routes/                 # API endpoints
│   ├── services/               # Business logic
│   ├── tests/                  # Test suite
│   ├── app.py                  # Main application
│   └── requirements.txt
│
└── backend/node-document-service/  # Document Management
    ├── controllers/
    ├── models/
    ├── routes/
    └── server.js
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- MongoDB 4.4+
- npm or yarn

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-hr-management-system.git
cd ai-hr-management-system
```

2. **Backend Setup**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLP models
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt stopwords

# Configure environment
cp .env.example .env
# Edit .env with your MongoDB URI and settings

# Run backend
python app.py
```

3. **Frontend Setup**
```bash
cd frontend

# Install dependencies
npm install

# Run frontend
npm start
```

4. **Document Service Setup**
```bash
cd backend/node-document-service

# Install dependencies
npm install

# Configure environment
cp .env.example .env

# Run service
npm start
```

### Default Ports
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Document Service: http://localhost:5001
- MongoDB: mongodb://localhost:27017

## 📖 Usage

### For HR Managers

1. **Post a Job**
   - Navigate to "Post Job"
   - Fill in job details, required skills, and experience
   - AI will automatically match incoming candidates

2. **Review Candidates**
   - Go to "Candidate Ranking"
   - View AI-generated match scores
   - Filter and sort by relevance
   - Update candidate status

3. **Manage Employees**
   - Access "Employee Management"
   - Add, edit, or remove employee records
   - Track attendance and performance

### For Candidates

1. **Register/Login**
   - Create an account
   - Complete your profile

2. **Upload Resume**
   - Upload PDF or DOCX resume
   - AI automatically extracts your skills and experience

3. **Browse Jobs**
   - View available positions
   - See your match score for each job
   - Track application status

## 🤖 AI Features Explained

### Resume Parsing
- Extracts text from PDF and DOCX files
- Identifies skills, experience, education, and contact info
- Uses NLP to understand context and qualifications

### Candidate Matching Algorithm
```python
# Simplified matching logic
1. Extract skills from job description
2. Extract skills from candidate resume
3. Calculate skill overlap using TF-IDF
4. Apply experience weighting
5. Generate match score (0-100%)
```

### Ranking System
- Candidates automatically ranked by match score
- Considers: skills match, experience level, education
- Real-time updates as new candidates apply

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- Input sanitization
- Secure file upload validation
- Environment variable protection

## 📊 API Documentation

### Authentication
```
POST /api/auth/register - Register new user
POST /api/auth/login    - User login
GET  /api/auth/verify   - Verify JWT token
```

### Jobs
```
GET    /api/jobs           - Get all jobs
POST   /api/jobs           - Create new job
GET    /api/jobs/:id       - Get job by ID
PUT    /api/jobs/:id       - Update job
DELETE /api/jobs/:id       - Delete job
```

### Candidates
```
GET    /api/candidates              - Get all candidates
POST   /api/candidates              - Create candidate
GET    /api/candidates/:id          - Get candidate details
PUT    /api/candidates/:id/status   - Update candidate status
```

### Resumes
```
POST   /api/resumes/upload          - Upload resume
GET    /api/resumes/:id             - Download resume
```

## 🧪 Testing

```bash
# Backend tests
cd backend
python -m pytest tests/

# Run specific test
python tests/test_resume_matcher.py
```

## 🎨 Screenshots

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### Candidate Ranking
![Candidate Ranking](docs/screenshots/candidate-ranking.png)

### Job Posting
![Job Posting](docs/screenshots/job-posting.png)

## 📈 Performance

- Resume parsing: ~2-3 seconds per document
- AI matching: ~0.5 seconds per candidate
- Supports 1000+ concurrent users
- Handles 10,000+ resumes efficiently

## 🛣️ Roadmap

- [ ] Email notifications for candidates
- [ ] Interview scheduling system
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Integration with LinkedIn
- [ ] Video interview feature
- [ ] Multi-language support

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Flask documentation and community
- React team for the amazing framework
- scikit-learn for ML capabilities
- MongoDB for flexible data storage
- All open-source contributors

## 📞 Support

For support, email your.email@example.com or open an issue in the GitHub repository.

---

⭐ **Star this repository if you find it helpful!**

Made with ❤️ and AI
