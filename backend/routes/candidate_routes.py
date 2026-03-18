from flask import Blueprint, request, jsonify
from models.candidate_model import Candidate
from models.job_model import Job
from services.candidate_service import CandidateService
from ai.resume_matcher import ResumeMatcher

candidate_bp = Blueprint('candidates', __name__)

@candidate_bp.route('/', methods=['GET'])
def get_candidates():
    try:
        # Get optional query parameters
        job_id = request.args.get('job_id')
        sort_by_score = request.args.get('sort_by_score', 'true').lower() == 'true'
        
        # Retrieve candidates
        if job_id:
            candidates = Candidate.find_by_job(job_id)
        else:
            candidates = Candidate.find_all()
        
        # Convert ObjectId to string and format response
        ranked_candidates = []
        matcher = ResumeMatcher()
        
        for candidate in candidates:
            # Get job details
            job = Job.find_by_id(candidate.get('job_id', ''))
            job_title = job.get('job_title', 'N/A') if job else 'N/A'
            
            # Recalculate match score if needed
            if job and candidate.get('resume_text'):
                match_score = matcher.calculate_match_score(
                    candidate.get('resume_text', ''),
                    job.get('required_skills', '') + ' ' + job.get('description', '')
                )
                # Update match score in database
                Candidate.update(str(candidate['_id']), {'match_score': match_score})
            else:
                match_score = candidate.get('match_score', 0)
            
            ranked_candidates.append({
                'candidate_id': str(candidate['_id']),
                'candidate_name': candidate.get('name', 'N/A'),
                'email': candidate.get('email', 'N/A'),
                'phone': candidate.get('phone', 'N/A'),
                'job_applied': job_title,
                'job_id': candidate.get('job_id', 'N/A'),
                'skills': candidate.get('skills', []),
                'experience': candidate.get('experience', 'N/A'),
                'match_score': round(match_score, 2),
                'status': candidate.get('status', 'pending'),
                'applied_at': candidate.get('applied_at').isoformat() if candidate.get('applied_at') else None
            })
        
        # Sort by match score (highest first)
        if sort_by_score:
            ranked_candidates.sort(key=lambda x: x['match_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'count': len(ranked_candidates),
            'candidates': ranked_candidates
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@candidate_bp.route('/<candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    try:
        candidate = Candidate.find_by_id(candidate_id)
        
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        # Get job details
        job = Job.find_by_id(candidate.get('job_id', ''))
        
        candidate['_id'] = str(candidate['_id'])
        if candidate.get('applied_at'):
            candidate['applied_at'] = candidate['applied_at'].isoformat()
        
        candidate['job_details'] = {
            'job_id': str(job['_id']) if job else None,
            'job_title': job.get('job_title', 'N/A') if job else 'N/A',
            'location': job.get('location', 'N/A') if job else 'N/A'
        } if job else None
        
        return jsonify({
            'success': True,
            'candidate': candidate
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@candidate_bp.route('/job/<job_id>', methods=['GET'])
def get_candidates_by_job(job_id):
    try:
        # Check if job exists
        job = Job.find_by_id(job_id)
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        # Get top candidates for this job
        limit = request.args.get('limit', 10, type=int)
        top_candidates = CandidateService.get_top_candidates(job_id, limit)
        
        # Format response
        ranked_candidates = []
        for candidate in top_candidates:
            ranked_candidates.append({
                'candidate_id': str(candidate['_id']),
                'candidate_name': candidate.get('name', 'N/A'),
                'email': candidate.get('email', 'N/A'),
                'phone': candidate.get('phone', 'N/A'),
                'job_applied': job.get('job_title', 'N/A'),
                'job_id': job_id,
                'skills': candidate.get('skills', []),
                'experience': candidate.get('experience', 'N/A'),
                'match_score': round(candidate.get('match_score', 0), 2),
                'status': candidate.get('status', 'pending'),
                'applied_at': candidate.get('applied_at').isoformat() if candidate.get('applied_at') else None
            })
        
        return jsonify({
            'success': True,
            'job_title': job.get('job_title', 'N/A'),
            'count': len(ranked_candidates),
            'candidates': ranked_candidates
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@candidate_bp.route('/', methods=['POST'])
def create_candidate():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'resume_text', 'job_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create candidate with AI matching
        candidate_id = CandidateService.create_with_matching(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            resume_text=data['resume_text'],
            skills=data.get('skills', []),
            experience=data.get('experience', ''),
            job_id=data['job_id']
        )
        
        return jsonify({
            'success': True,
            'message': 'Candidate created successfully',
            'candidate_id': candidate_id
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@candidate_bp.route('/<candidate_id>', methods=['PUT'])
def update_candidate(candidate_id):
    try:
        data = request.json
        
        # Check if candidate exists
        candidate = Candidate.find_by_id(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        # Update candidate
        Candidate.update(candidate_id, data)
        
        return jsonify({
            'success': True,
            'message': 'Candidate updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@candidate_bp.route('/<candidate_id>/status', methods=['PUT', 'PATCH'])
def update_candidate_status(candidate_id):
    try:
        data = request.json
        status = data.get('status')
        
        if not status:
            return jsonify({'error': 'status is required'}), 400
        
        # Validate status
        valid_statuses = ['pending', 'shortlisted', 'interviewed', 'rejected', 'hired']
        if status not in valid_statuses:
            return jsonify({'error': f'Invalid status. Must be one of: {valid_statuses}'}), 400
        
        # Update status
        result = CandidateService.update_candidate_status(candidate_id, status)
        
        if result.matched_count == 0:
            return jsonify({'error': 'Candidate not found'}), 404
        
        return jsonify({
            'success': True,
            'message': f'Candidate status updated to {status}'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@candidate_bp.route('/<candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id):
    try:
        # Check if candidate exists
        candidate = Candidate.find_by_id(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        # Delete candidate
        Candidate.delete(candidate_id)
        
        return jsonify({
            'success': True,
            'message': 'Candidate deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@candidate_bp.route('/<candidate_id>/resume', methods=['GET'])
def download_resume(candidate_id):
    try:
        from flask import send_file
        import os
        
        candidate = Candidate.find_by_id(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        resume_file = candidate.get('resume_file')
        if not resume_file or not os.path.exists(resume_file):
            return jsonify({'error': 'Resume file not found'}), 404
        
        return send_file(resume_file, as_attachment=True)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
