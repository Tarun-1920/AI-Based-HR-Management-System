from bson import ObjectId
from datetime import datetime
from database import get_collection

faqs_collection = get_collection('faqs')

class FAQ:
    @staticmethod
    def find_all():
        return list(faqs_collection.find())

    @staticmethod
    def search_by_keywords(keywords):
        query = {'keywords': {'$in': keywords}}
        return list(faqs_collection.find(query))

    @staticmethod
    def seed_default_faqs():
        if faqs_collection.count_documents({}) == 0:
            faqs = [
                # HR-related FAQs
                {'question': 'What is the leave policy?', 'answer': 'Employees get 20 days paid leave per year. Apply through employee portal.', 'category': 'Leave', 'keywords': ['leave', 'vacation', 'time off', 'pto', 'paid leave'], 'role': 'hr'},
                {'question': 'What are company holidays?', 'answer': 'Company holidays include New Year, Independence Day, Thanksgiving, Christmas.', 'category': 'Holidays', 'keywords': ['holiday', 'holidays', 'off days', 'public holiday'], 'role': 'hr'},
                {'question': 'What is work from home policy?', 'answer': 'Employees can WFH 2 days per week with manager approval.', 'category': 'WFH', 'keywords': ['wfh', 'work from home', 'remote', 'hybrid'], 'role': 'hr'},
                {'question': 'When is salary paid?', 'answer': 'Salaries paid on last working day of each month via direct deposit.', 'category': 'Salary', 'keywords': ['salary', 'payment', 'payroll', 'pay', 'compensation'], 'role': 'hr'},
                {'question': 'How to contact HR?', 'answer': 'Contact HR at hr@company.com or call +1-555-0100. Hours: Mon-Fri 9AM-5PM.', 'category': 'Contact', 'keywords': ['contact', 'hr', 'email', 'phone', 'reach'], 'role': 'both'},
                
                # Candidate-related FAQs
                {'question': 'What jobs are currently available?', 'answer': 'We have various positions open across different departments. Please visit the Browse Jobs page to see all current openings with detailed descriptions and requirements.', 'category': 'Jobs', 'keywords': ['jobs', 'available', 'openings', 'positions', 'vacancies', 'hiring'], 'role': 'candidate'},
                {'question': 'How can I improve my job application?', 'answer': 'To improve your application: 1) Tailor your resume to match job requirements, 2) Highlight relevant skills and achievements, 3) Use action verbs, 4) Keep it concise (1-2 pages), 5) Proofread carefully for errors.', 'category': 'Application', 'keywords': ['application', 'improve', 'tips', 'better', 'enhance', 'apply'], 'role': 'candidate'},
                {'question': 'What should I include in my resume?', 'answer': 'Your resume should include: 1) Contact information, 2) Professional summary, 3) Work experience with achievements, 4) Education, 5) Technical and soft skills, 6) Certifications (if any), 7) Projects or portfolio links.', 'category': 'Resume', 'keywords': ['resume', 'cv', 'include', 'add', 'write', 'format'], 'role': 'candidate'},
                {'question': 'Can you give me interview preparation tips?', 'answer': 'Interview tips: 1) Research the company thoroughly, 2) Practice common interview questions, 3) Prepare STAR method examples, 4) Dress professionally, 5) Arrive 10-15 minutes early, 6) Prepare questions to ask, 7) Follow up with a thank-you email.', 'category': 'Interview', 'keywords': ['interview', 'preparation', 'tips', 'prepare', 'questions', 'ready'], 'role': 'candidate'},
                {'question': 'How long does the hiring process take?', 'answer': 'Our typical hiring process takes 2-4 weeks and includes: 1) Application review (3-5 days), 2) Initial screening call (1 week), 3) Technical/skills assessment, 4) Final interview, 5) Offer decision. We keep candidates updated throughout.', 'category': 'Process', 'keywords': ['hiring', 'process', 'timeline', 'long', 'take', 'duration', 'time'], 'role': 'candidate'},
                {'question': 'What skills are most in demand?', 'answer': 'Currently, we are looking for candidates with skills in: Python, JavaScript, React, Node.js, AWS, Docker, SQL, Machine Learning, Data Analysis, and strong communication skills. Check specific job postings for detailed requirements.', 'category': 'Skills', 'keywords': ['skills', 'demand', 'required', 'need', 'looking', 'technologies'], 'role': 'candidate'},
                {'question': 'How do I track my application status?', 'answer': 'You can track your application status on your Dashboard. It shows all your submitted applications with current status (Applied, Under Review, Shortlisted, Interviewed). You will also receive email notifications for status updates.', 'category': 'Status', 'keywords': ['track', 'status', 'application', 'check', 'progress', 'update'], 'role': 'candidate'},
                {'question': 'What is the salary range for positions?', 'answer': 'Salary ranges vary by position, experience level, and location. Many of our job postings include salary information. We offer competitive compensation packages including benefits, health insurance, and performance bonuses.', 'category': 'Compensation', 'keywords': ['salary', 'range', 'pay', 'compensation', 'benefits', 'package'], 'role': 'candidate'},
            ]
            for faq in faqs:
                faq['created_at'] = datetime.utcnow()
                faqs_collection.insert_one(faq)
