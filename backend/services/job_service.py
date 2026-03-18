from models.job_model import Job

class JobService:
    @staticmethod
    def get_active_jobs():
        jobs = Job.find_all()
        return [job for job in jobs if job.get('status') == 'open']

    @staticmethod
    def close_job(job_id):
        return Job.update(job_id, {'status': 'closed'})

    @staticmethod
    def reopen_job(job_id):
        return Job.update(job_id, {'status': 'open'})
