EMAIL_TEMPLATES = {
    'application_received': {
        'subject': 'Application Received - {job_title}',
        'body': '''Dear {candidate_name},

Thank you for applying for the {job_title} position at our company.

We have received your application and our team is currently reviewing it. We appreciate your interest in joining our organization.

You will hear from us within 5-7 business days regarding the next steps in the recruitment process.

Best regards,
HR Team'''
    },
    
    'interview_invitation': {
        'subject': 'Interview Invitation - {job_title}',
        'body': '''Dear {candidate_name},

Congratulations! We are pleased to invite you for an interview for the {job_title} position.

Interview Details:
- Date: {interview_date}
- Time: {interview_time}
- Location: {interview_location}
- Interviewer: {interviewer_name}

Please confirm your availability by replying to this email.

We look forward to meeting you!

Best regards,
HR Team'''
    },
    
    'interview_feedback': {
        'subject': 'Interview Feedback - {job_title}',
        'body': '''Dear {candidate_name},

Thank you for taking the time to interview with us for the {job_title} position.

{feedback_message}

We appreciate your interest in our company and wish you the best in your career.

Best regards,
HR Team'''
    },
    
    'rejection': {
        'subject': 'Application Status Update - {job_title}',
        'body': '''Dear {candidate_name},

Thank you for your interest in the {job_title} position and for taking the time to apply.

After careful consideration, we have decided to move forward with other candidates whose qualifications more closely match our current needs.

We appreciate your interest in our company and encourage you to apply for future opportunities that match your skills and experience.

We wish you the best in your job search.

Best regards,
HR Team'''
    },
    
    'offer_letter': {
        'subject': 'Job Offer - {job_title}',
        'body': '''Dear {candidate_name},

We are delighted to offer you the position of {job_title} at our company!

Offer Details:
- Position: {job_title}
- Start Date: {start_date}
- Salary: {salary}
- Location: {location}

Please review the attached offer letter and respond within 5 business days to confirm your acceptance.

We are excited to have you join our team!

Best regards,
HR Team'''
    },
    
    'interview_reminder': {
        'subject': 'Interview Reminder - {job_title}',
        'body': '''Dear {candidate_name},

This is a friendly reminder about your upcoming interview for the {job_title} position.

Interview Details:
- Date: {interview_date}
- Time: {interview_time}
- Location: {interview_location}

Please arrive 10 minutes early and bring a copy of your resume.

Looking forward to meeting you!

Best regards,
HR Team'''
    }
}

def get_template(template_type):
    return EMAIL_TEMPLATES.get(template_type, None)

def format_template(template_type, **kwargs):
    template = get_template(template_type)
    if not template:
        return None
    
    subject = template['subject'].format(**kwargs)
    body = template['body'].format(**kwargs)
    
    return {
        'subject': subject,
        'body': body
    }
