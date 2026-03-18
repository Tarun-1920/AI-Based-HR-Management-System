from flask import Blueprint, request, jsonify
from models.communication_model import Communication
from models.candidate_model import Candidate
from models.job_model import Job
from utils.email_templates import format_template
from datetime import datetime
from bson import ObjectId

communication_bp = Blueprint('communications', __name__)

@communication_bp.route('/send', methods=['POST'])
def send_communication():
    """
    Send email/message to candidate
    
    Required: candidate_id, template_type
    Optional: custom_message, metadata
    """
    try:
        data = request.get_json()
        
        candidate_id = data.get('candidate_id')
        template_type = data.get('template_type')
        custom_data = data.get('custom_data', {})
        
        if not candidate_id or not template_type:
            return jsonify({'error': 'candidate_id and template_type are required'}), 400
        
        # Get candidate details
        candidate = Candidate.find_by_id(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        # Get job details
        job = Job.find_by_id(candidate.get('job_id', ''))
        
        # Prepare template data
        template_data = {
            'candidate_name': candidate.get('name', 'Candidate'),
            'job_title': job.get('job_title', 'Position') if job else 'Position',
            **custom_data
        }
        
        # Format email template
        formatted = format_template(template_type, **template_data)
        if not formatted:
            return jsonify({'error': 'Invalid template type'}), 400
        
        # Create communication record
        communication_id = Communication.create(
            candidate_id=candidate_id,
            candidate_email=candidate.get('email'),
            template_type=template_type,
            subject=formatted['subject'],
            message=formatted['body'],
            metadata=custom_data
        )
        
        return jsonify({
            'success': True,
            'message': 'Communication sent successfully',
            'communication_id': communication_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@communication_bp.route('/schedule-interview', methods=['POST'])
def schedule_interview():
    """
    Schedule interview and send notification
    
    Required: candidate_id, interview_date, interview_time, interview_location
    """
    try:
        data = request.get_json()
        
        candidate_id = data.get('candidate_id')
        interview_date = data.get('interview_date')
        interview_time = data.get('interview_time')
        interview_location = data.get('interview_location')
        interviewer_name = data.get('interviewer_name', 'HR Team')
        
        if not all([candidate_id, interview_date, interview_time, interview_location]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Get candidate details
        candidate = Candidate.find_by_id(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        # Get job details
        job = Job.find_by_id(candidate.get('job_id', ''))
        
        # Prepare interview data
        interview_data = {
            'candidate_name': candidate.get('name', 'Candidate'),
            'job_title': job.get('job_title', 'Position') if job else 'Position',
            'interview_date': interview_date,
            'interview_time': interview_time,
            'interview_location': interview_location,
            'interviewer_name': interviewer_name
        }
        
        # Format interview invitation email
        formatted = format_template('interview_invitation', **interview_data)
        
        # Create communication record
        communication_id = Communication.create(
            candidate_id=candidate_id,
            candidate_email=candidate.get('email'),
            template_type='interview_invitation',
            subject=formatted['subject'],
            message=formatted['body'],
            scheduled_date=f"{interview_date} {interview_time}",
            metadata=interview_data
        )
        
        # Update candidate status
        Candidate.update(candidate_id, {'status': 'interviewed'})
        
        return jsonify({
            'success': True,
            'message': 'Interview scheduled and notification sent',
            'communication_id': communication_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@communication_bp.route('/history/<candidate_id>', methods=['GET'])
def get_communication_history(candidate_id):
    """
    Get communication history for a candidate
    """
    try:
        communications = Communication.find_by_candidate(candidate_id)
        
        # Format response
        history = []
        for comm in communications:
            history.append({
                'id': str(comm['_id']),
                'template_type': comm.get('template_type'),
                'subject': comm.get('subject'),
                'message': comm.get('message'),
                'sent_at': comm.get('sent_at').isoformat() if comm.get('sent_at') else None,
                'scheduled_date': comm.get('scheduled_date'),
                'status': comm.get('status'),
                'metadata': comm.get('metadata', {})
            })
        
        return jsonify({
            'success': True,
            'count': len(history),
            'communications': history
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@communication_bp.route('/all', methods=['GET'])
def get_all_communications():
    """
    Get all communications
    """
    try:
        communications = Communication.find_all()
        
        # Format response
        all_comms = []
        for comm in communications:
            # Get candidate name
            candidate = Candidate.find_by_id(comm.get('candidate_id'))
            candidate_name = candidate.get('name', 'Unknown') if candidate else 'Unknown'
            
            all_comms.append({
                'id': str(comm['_id']),
                'candidate_id': comm.get('candidate_id'),
                'candidate_name': candidate_name,
                'candidate_email': comm.get('candidate_email'),
                'template_type': comm.get('template_type'),
                'subject': comm.get('subject'),
                'sent_at': comm.get('sent_at').isoformat() if comm.get('sent_at') else None,
                'scheduled_date': comm.get('scheduled_date'),
                'status': comm.get('status')
            })
        
        return jsonify({
            'success': True,
            'count': len(all_comms),
            'communications': all_comms
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@communication_bp.route('/templates', methods=['GET'])
def get_templates():
    """
    Get available email templates
    """
    try:
        from utils.email_templates import EMAIL_TEMPLATES
        
        templates = []
        for key, value in EMAIL_TEMPLATES.items():
            templates.append({
                'type': key,
                'name': key.replace('_', ' ').title(),
                'subject': value['subject'],
                'body': value['body']
            })
        
        return jsonify({
            'success': True,
            'templates': templates
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
