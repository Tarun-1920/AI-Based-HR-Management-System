from models.candidate_model import Candidate
from models.job_model import Job
from ai.resume_matcher import ResumeMatcher
from database import get_collection
from bson import ObjectId

class CandidateService:
    @staticmethod
    def create_with_matching(name, email, phone, resume_text, skills, experience, job_id):
        job = Job.find_by_id(job_id)
        if not job:
            raise ValueError('Job not found')
        
        matcher = ResumeMatcher()
        match_score = matcher.calculate_match_score(resume_text, job['requirements'])
        
        candidate_id = Candidate.create(name, email, phone, resume_text, skills, experience, job_id)
        Candidate.update(candidate_id, {'match_score': match_score})
        
        return candidate_id

    @staticmethod
    def get_top_candidates(job_id, limit=10):
        candidates = Candidate.find_by_job(job_id)
        sorted_candidates = sorted(candidates, key=lambda x: x.get('match_score', 0), reverse=True)
        return sorted_candidates[:limit]

    @staticmethod
    def update_candidate_status(candidate_id, status):
        return Candidate.update(candidate_id, {'status': status})

    @staticmethod
    def get_candidates():
        candidates = get_collection('candidates')
        results = []
        for doc in candidates.find():
            results.append({
                'candidate_name': doc.get('candidate_name'),
                'email': doc.get('email'),
                'skills': doc.get('skills'),
                'resume_file': doc.get('resume_file'),
                '_id': str(doc['_id'])
            })
        return results

    @staticmethod
    def update_match_score(candidate_id, match_score):
        candidates = get_collection('candidates')
        result = candidates.update_one(
            {'_id': ObjectId(candidate_id)},
            {'$set': {'match_score': match_score}}
        )
        return result.modified_count > 0
