from flask import Blueprint, request, jsonify
from ai.resume_matcher import ResumeMatcher
from ai.resume_parser import extract_resume_text, get_file_info
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from utils import (
    validate_required_fields,
    validate_email,
    validate_object_id,
    success_response,
    error_response,
    sanitize_string
)

resume_bp = Blueprint('resumes', __name__)

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file_size(file):
    """Check if file size is within limit."""
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size <= MAX_FILE_SIZE

@resume_bp.route('/upload-resume', methods=['POST'])
def upload_resume():
    """
    Upload candidate resume file.
    
    Required fields: candidate_name, email, job_id, resume (file)
    
    Returns:
        201: Resume uploaded successfully
        400: Validation error
        413: File too large
        500: Server error
    """
    try:
        print(f"Upload resume request received")  # Debug log
        print(f"Files: {request.files}")  # Debug log
        print(f"Form data: {request.form}")  # Debug log
        
        # Validate file presence
        if 'resume' not in request.files:
            print("Error: No resume file in request")  # Debug log
            return error_response('No resume file provided', 400)
        
        file = request.files['resume']
        # Handle both frontend and backend field names
        first_name = request.form.get('firstName') or request.form.get('first_name')
        last_name = request.form.get('lastName') or request.form.get('last_name')
        candidate_name = request.form.get('candidate_name')
        
        # Combine first and last name if provided separately
        if not candidate_name and first_name:
            candidate_name = f"{first_name} {last_name}" if last_name else first_name
        
        email = request.form.get('email')
        job_id = request.form.get('job_id') or request.form.get('jobId')
        phone = request.form.get('phone')
        experience = request.form.get('experience')
        location = request.form.get('location') or request.form.get('preferredLocation')
        expected_salary = request.form.get('expectedSalary') or request.form.get('expected_salary')
        
        print(f"Candidate: {candidate_name}, Email: {email}, Job ID: {job_id}")  # Debug log
        
        # Validate required form fields
        if not candidate_name or not email or not job_id:
            print(f"Error: Missing required fields - Name: {candidate_name}, Email: {email}, Job: {job_id}")  # Debug log
            return error_response('candidate_name, email, and job_id are required', 400)
        
        # Sanitize inputs
        candidate_name = sanitize_string(candidate_name, 100)
        email = sanitize_string(email.lower(), 255)
        job_id = sanitize_string(job_id, 24)
        
        # Validate email format
        if not validate_email(email):
            return error_response('Invalid email format', 400)
        
        # Validate job ID format
        if not validate_object_id(job_id):
            return error_response('Invalid job ID format', 400)
        
        # Check if file is selected
        if file.filename == '':
            return error_response('No file selected', 400)
        
        # Validate file type
        if not allowed_file(file.filename):
            return error_response('Only PDF and DOCX files are allowed', 400)
        
        # Validate file size
        if not validate_file_size(file):
            return error_response(f'File size exceeds maximum limit of {MAX_FILE_SIZE / 1024 / 1024}MB', 413)
        
        # Generate secure filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        original_filename = secure_filename(file.filename)
        filename = f"{timestamp}_{email.replace('@', '_')}_{original_filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Save file to uploads folder
        file.save(filepath)
        
        # Extract text from resume
        try:
            resume_text = extract_resume_text(filepath)
            text_preview = resume_text[:200] + '...' if len(resume_text) > 200 else resume_text
            text_length = len(resume_text)
        except Exception as e:
            resume_text = ""
            text_preview = f"Error extracting text: {str(e)}"
            text_length = 0
        
        # Create candidate record in database
        from models.candidate_model import Candidate
        from models.job_model import Job
        
        # Get job details
        job = Job.find_by_id(job_id)
        if not job:
            return error_response('Job not found', 404)
        
        # Calculate match score
        try:
            from ai.resume_matcher import ResumeMatcher
            matcher = ResumeMatcher()
            match_score = matcher.calculate_match_score(
                resume_text,
                job.get('required_skills', '') + ' ' + job.get('description', '')
            )
        except Exception as e:
            print(f"Error calculating match score: {str(e)}")
            match_score = 0
        
        # Extract skills from resume
        try:
            skills = matcher.extract_skills(resume_text)
        except:
            skills = []
        
        # Create candidate
        candidate_id = Candidate.create(
            name=candidate_name,
            email=email,
            phone=phone or '',
            resume_text=resume_text,
            skills=skills,
            experience=experience or '',
            job_id=job_id
        )
        
        # Update with match score and resume file path
        Candidate.update(candidate_id, {
            'match_score': match_score,
            'resume_file': filepath,
            'location': location or '',
            'expected_salary': expected_salary or ''
        })
        
        print(f"Candidate created with ID: {candidate_id}, Match Score: {match_score}")
        
        return success_response(
            message='Resume uploaded successfully',
            data={
                'candidate_id': candidate_id,
                'candidate_name': candidate_name,
                'email': email,
                'job_id': job_id,
                'match_score': match_score,
                'filename': filename,
                'filepath': filepath,
                'text_preview': text_preview,
                'text_length': text_length
            },
            status_code=201
        )
        
    except Exception as e:
        return error_response(f'Failed to upload resume: {str(e)}', 500)

@resume_bp.route('/parse', methods=['POST'])
def parse_resume():
    """
    Parse resume file and extract text and skills.
    
    Required: resume file (PDF or DOCX)
    cd
    Returns:
        200: Resume parsed successfully
        400: Validation error
        413: File too large
        500: Server error
    """
    try:
        # Check if file is provided
        if 'resume' not in request.files:
            return error_response('No resume file provided', 400)
        
        file = request.files['resume']
        
        if file.filename == '':
            return error_response('No file selected', 400)
        
        if not allowed_file(file.filename):
            return error_response('Only PDF and DOCX files are allowed', 400)
        
        if not validate_file_size(file):
            return error_response(f'File size exceeds maximum limit of {MAX_FILE_SIZE / 1024 / 1024}MB', 413)
        
        # Save temporarily
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"temp_{timestamp}_{secure_filename(file.filename)}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Extract text
        resume_text = extract_resume_text(filepath)
        file_info = get_file_info(filepath)
        
        # Extract skills
        matcher = ResumeMatcher()
        skills = matcher.extract_skills(resume_text)
        
        return success_response(
            message='Resume parsed successfully',
            data={
                'text': resume_text,
                'skills': skills,
                'file_info': file_info
            },
            status_code=200
        )
        
    except Exception as e:
        return error_response(f'Failed to parse resume: {str(e)}', 500)

@resume_bp.route('/match', methods=['POST'])
def match_resume():
    """
    Calculate match score between resume and job description.
    
    Required fields: resume_text, job_requirements
    
    Returns:
        200: Match score calculated
        400: Validation error
        500: Server error
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        is_valid, error_msg = validate_required_fields(data, ['resume_text', 'job_requirements'])
        if not is_valid:
            return error_response(error_msg, 400)
        
        resume_text = data['resume_text']
        job_requirements = data['job_requirements']
        
        # Validate text length
        if len(resume_text) < 50:
            return error_response('Resume text is too short (minimum 50 characters)', 400)
        
        if len(job_requirements) < 20:
            return error_response('Job requirements text is too short (minimum 20 characters)', 400)
        
        # Calculate match score
        matcher = ResumeMatcher()
        score = matcher.calculate_match_score(resume_text, job_requirements)
        
        return success_response(
            message=f'Resume matches job requirements by {score}%',
            data={'match_score': score},
            status_code=200
        )
        
    except Exception as e:
        return error_response(f'Failed to calculate match score: {str(e)}', 500)

@resume_bp.route('/detailed-match', methods=['POST'])
def detailed_match():
    """
    Get detailed match analysis including skills breakdown.
    
    Required fields: resume_text, job_requirements
    
    Returns:
        200: Detailed analysis
        400: Validation error
        500: Server error
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        is_valid, error_msg = validate_required_fields(data, ['resume_text', 'job_requirements'])
        if not is_valid:
            return error_response(error_msg, 400)
        
        resume_text = data['resume_text']
        job_requirements = data['job_requirements']
        
        # Validate text length
        if len(resume_text) < 50:
            return error_response('Resume text is too short (minimum 50 characters)', 400)
        
        if len(job_requirements) < 20:
            return error_response('Job requirements text is too short (minimum 20 characters)', 400)
        
        # Get detailed analysis
        matcher = ResumeMatcher()
        analysis = matcher.get_detailed_match_analysis(resume_text, job_requirements)
        
        return success_response(
            data={'analysis': analysis},
            status_code=200
        )
        
    except Exception as e:
        return error_response(f'Failed to perform detailed analysis: {str(e)}', 500)

@resume_bp.route('/extract-skills', methods=['POST'])
def extract_skills():
    """
    Extract skills from resume text.
    
    Required fields: resume_text
    
    Returns:
        200: Skills extracted
        400: Validation error
        500: Server error
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        is_valid, error_msg = validate_required_fields(data, ['resume_text'])
        if not is_valid:
            return error_response(error_msg, 400)
        
        resume_text = data['resume_text']
        
        # Validate text length
        if len(resume_text) < 20:
            return error_response('Resume text is too short (minimum 20 characters)', 400)
        
        # Extract skills
        matcher = ResumeMatcher()
        skills = matcher.extract_skills(resume_text)
        
        return success_response(
            data={'skills': skills, 'count': len(skills)},
            status_code=200
        )
        
    except Exception as e:
        return error_response(f'Failed to extract skills: {str(e)}', 500)
