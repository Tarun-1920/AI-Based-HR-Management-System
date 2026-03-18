from flask import Blueprint, request, jsonify
from bson import ObjectId
from models.job_model import Job
from services.job_service import JobService
from utils import (
    validate_required_fields,
    validate_object_id,
    success_response,
    error_response,
    sanitize_string
)

job_bp = Blueprint('jobs', __name__)

@job_bp.route('/', methods=['GET'])
def get_jobs():
    """
    Get all jobs with optional filtering.
    
    Query params:
        status: Filter by status (open/closed)
        limit: Limit number of results
    
    Returns:
        200: List of jobs
        500: Server error
    """
    try:
        # Get query parameters
        status_filter = request.args.get('status')
        limit = request.args.get('limit', type=int)
        
        # Retrieve jobs
        jobs = Job.find_all()
        
        # Apply status filter
        if status_filter:
            jobs = [job for job in jobs if job.get('status') == status_filter]
        
        # Convert ObjectId to string and format dates
        for job in jobs:
            job['_id'] = str(job['_id'])
            if 'created_at' in job:
                job['created_at'] = job['created_at'].isoformat()
        
        # Apply limit
        if limit and limit > 0:
            jobs = jobs[:limit]
        
        return success_response(
            data={'count': len(jobs), 'jobs': jobs},
            status_code=200
        )
        
    except Exception as e:
        return error_response(f'Failed to retrieve jobs: {str(e)}', 500)

@job_bp.route('/<job_id>', methods=['GET'])
def get_job(job_id):
    """
    Get a single job by ID.
    
    Returns:
        200: Job details
        400: Invalid job ID format
        404: Job not found
        500: Server error
    """
    try:
        # Validate job ID format
        if not validate_object_id(job_id):
            return error_response('Invalid job ID format', 400)
        
        # Find job
        job = Job.find_by_id(job_id)
        
        if not job:
            return error_response('Job not found', 404)
        
        # Format response
        job['_id'] = str(job['_id'])
        if 'created_at' in job:
            job['created_at'] = job['created_at'].isoformat()
        
        return success_response(
            data={'job': job},
            status_code=200
        )
        
    except Exception as e:
        return error_response(f'Failed to retrieve job: {str(e)}', 500)

@job_bp.route('/', methods=['POST'], strict_slashes=False)
def create_job():
    """
    Create a new job posting.
    
    Required fields: job_title or title, description, required_skills, experience or experience_required, location
    Optional fields: salary_range or salary
    
    Returns:
        201: Job created successfully
        400: Validation error
        500: Server error
    """
    try:
        data = request.get_json()
        print(f"Received job data: {data}")  # Debug log
        
        # Handle both frontend and backend field names
        job_title = data.get('job_title') or data.get('title')
        description = data.get('description')
        required_skills = data.get('required_skills')
        experience = data.get('experience') or data.get('experience_required')
        location = data.get('location')
        salary_range = data.get('salary_range') or data.get('salary') or ''
        
        # Convert skills array to string if needed
        if isinstance(required_skills, list):
            required_skills = ', '.join(required_skills)
        
        # Validate required fields manually
        if not job_title:
            print("Validation error: job_title is required")  # Debug log
            return error_response('job_title or title is required', 400)
        if not description:
            print("Validation error: description is required")  # Debug log
            return error_response('description is required', 400)
        if not required_skills:
            print("Validation error: required_skills is required")  # Debug log
            return error_response('required_skills is required', 400)
        if not experience:
            print("Validation error: experience is required")  # Debug log
            return error_response('experience or experience_required is required', 400)
        if not location:
            print("Validation error: location is required")  # Debug log
            return error_response('location is required', 400)
        
        # Sanitize inputs
        job_title = sanitize_string(job_title, 200)
        description = sanitize_string(description, 5000)
        required_skills = sanitize_string(required_skills, 1000)
        experience = sanitize_string(experience, 100)
        location = sanitize_string(location, 200)
        salary_range = sanitize_string(salary_range, 100)
        
        # Validate field lengths
        if len(job_title) < 3:
            return error_response('Job title must be at least 3 characters', 400)
        
        if len(description) < 10:
            return error_response('Description must be at least 10 characters', 400)
        
        # Create job
        job_id = Job.create(
            title=job_title,
            description=description,
            requirements=required_skills,
            location=location,
            experience=experience,
            salary_range=salary_range
        )
        
        print(f"Job created successfully with ID: {job_id}")  # Debug log
        
        return success_response(
            message='Job created successfully',
            data={'job_id': job_id, 'jobId': job_id},
            status_code=201
        )
        
    except Exception as e:
        print(f"Error creating job: {str(e)}")  # Debug log
        import traceback
        traceback.print_exc()
        return error_response(f'Failed to create job: {str(e)}', 500)

@job_bp.route('/<job_id>', methods=['PUT'])
def update_job(job_id):
    """
    Update an existing job.
    
    Returns:
        200: Job updated successfully
        400: Invalid job ID or validation error
        404: Job not found
        500: Server error
    """
    try:
        # Validate job ID format
        if not validate_object_id(job_id):
            return error_response('Invalid job ID format', 400)
        
        # Check if job exists
        job = Job.find_by_id(job_id)
        if not job:
            return error_response('Job not found', 404)
        
        data = request.get_json()
        
        if not data:
            return error_response('Request body is required', 400)
        
        # Sanitize inputs if provided
        update_data = {}
        
        if 'job_title' in data:
            update_data['job_title'] = sanitize_string(data['job_title'], 200)
            if len(update_data['job_title']) < 3:
                return error_response('Job title must be at least 3 characters', 400)
        
        if 'description' in data:
            update_data['description'] = sanitize_string(data['description'], 5000)
        
        if 'required_skills' in data:
            update_data['required_skills'] = sanitize_string(data['required_skills'], 1000)
        
        if 'experience' in data:
            update_data['experience'] = sanitize_string(data['experience'], 100)
        
        if 'location' in data:
            update_data['location'] = sanitize_string(data['location'], 200)
        
        if 'salary_range' in data:
            update_data['salary_range'] = sanitize_string(data['salary_range'], 100)
        
        if 'status' in data:
            if data['status'] not in ['open', 'closed']:
                return error_response('Status must be either "open" or "closed"', 400)
            update_data['status'] = data['status']
        
        # Update job
        result = Job.update(job_id, update_data)
        
        if result.matched_count == 0:
            return error_response('Job not found', 404)
        
        return success_response(
            message='Job updated successfully',
            status_code=200
        )
        
    except Exception as e:
        return error_response(f'Failed to update job: {str(e)}', 500)

@job_bp.route('/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    """
    Delete a job posting.
    
    Returns:
        200: Job deleted successfully
        400: Invalid job ID format
        404: Job not found
        500: Server error
    """
    try:
        # Validate job ID format
        if not validate_object_id(job_id):
            return error_response('Invalid job ID format', 400)
        
        # Check if job exists
        job = Job.find_by_id(job_id)
        if not job:
            return error_response('Job not found', 404)
        
        # Delete job
        result = Job.delete(job_id)
        
        if result.deleted_count == 0:
            return error_response('Job not found', 404)
        
        return success_response(
            message='Job deleted successfully',
            status_code=200
        )
        
    except Exception as e:
        return error_response(f'Failed to delete job: {str(e)}', 500)

@job_bp.route('/active', methods=['GET'])
def get_active_jobs():
    """
    Get all active (open) jobs.
    
    Returns:
        200: List of active jobs
        500: Server error
    """
    try:
        jobs = JobService.get_active_jobs()
        
        # Format response
        for job in jobs:
            job['_id'] = str(job['_id'])
            if 'created_at' in job:
                job['created_at'] = job['created_at'].isoformat()
        
        return success_response(
            data={'count': len(jobs), 'jobs': jobs},
            status_code=200
        )
        
    except Exception as e:
        return error_response(f'Failed to retrieve active jobs: {str(e)}', 500)
