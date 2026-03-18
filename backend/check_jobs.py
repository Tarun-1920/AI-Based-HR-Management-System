"""
Quick script to check jobs in database
"""
from pymongo import MongoClient
from config import Config

try:
    client = MongoClient(Config.MONGO_URI)
    db = client[Config.DATABASE_NAME]
    jobs_collection = db['jobs']
    
    count = jobs_collection.count_documents({})
    print(f"Total jobs in database: {count}")
    
    if count > 0:
        print("\nJobs found:")
        for job in jobs_collection.find().limit(5):
            print(f"  - {job.get('job_title', 'N/A')} (ID: {job['_id']})")
    else:
        print("\nNo jobs found. Run 'python insert_sample_jobs.py' to add jobs.")
    
    client.close()
except Exception as e:
    print(f"Error: {e}")
