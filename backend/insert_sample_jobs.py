"""
Script to insert sample job postings into the database.
Run this script to populate the jobs collection with sample data.

Usage: python insert_sample_jobs.py
"""

from pymongo import MongoClient
from datetime import datetime
from config import Config

# Sample job postings
SAMPLE_JOBS = [
    {
        "job_title": "Senior Python Developer",
        "description": "We are looking for an experienced Python developer to join our backend team. You will be responsible for developing scalable web applications, APIs, and microservices. Strong knowledge of Python frameworks and databases required.",
        "required_skills": "Python, Django, Flask, PostgreSQL, REST API, Docker, AWS, Git",
        "experience": "5+ years",
        "location": "San Francisco, CA (Remote Available)",
        "salary_range": "$120,000 - $160,000",
        "status": "open",
        "created_at": datetime.utcnow()
    },
    {
        "job_title": "Full Stack Developer",
        "description": "Join our dynamic team as a Full Stack Developer. You'll work on both frontend and backend technologies, building modern web applications. Experience with React and Node.js is essential.",
        "required_skills": "React, Node.js, JavaScript, TypeScript, MongoDB, Express, HTML, CSS, Git",
        "experience": "3-5 years",
        "location": "New York, NY (Hybrid)",
        "salary_range": "$100,000 - $140,000",
        "status": "open",
        "created_at": datetime.utcnow()
    },
    {
        "job_title": "Data Analyst",
        "description": "We're seeking a Data Analyst to transform data into actionable insights. You will work with large datasets, create visualizations, and support business decision-making through data-driven analysis.",
        "required_skills": "Python, SQL, Tableau, Excel, Power BI, Statistics, Data Visualization, Pandas",
        "experience": "2-4 years",
        "location": "Austin, TX (On-site)",
        "salary_range": "$75,000 - $95,000",
        "status": "open",
        "created_at": datetime.utcnow()
    },
    {
        "job_title": "DevOps Engineer",
        "description": "Looking for a DevOps Engineer to manage our cloud infrastructure and CI/CD pipelines. You'll work with containerization, orchestration, and automation tools to ensure smooth deployments.",
        "required_skills": "AWS, Docker, Kubernetes, Jenkins, Terraform, Linux, Python, CI/CD, Git",
        "experience": "4-6 years",
        "location": "Seattle, WA (Remote)",
        "salary_range": "$130,000 - $170,000",
        "status": "open",
        "created_at": datetime.utcnow()
    },
    {
        "job_title": "Frontend Developer",
        "description": "We need a talented Frontend Developer to create beautiful, responsive user interfaces. You'll work closely with designers and backend developers to deliver exceptional user experiences.",
        "required_skills": "React, JavaScript, TypeScript, HTML5, CSS3, SASS, Redux, Webpack, Responsive Design",
        "experience": "2-4 years",
        "location": "Boston, MA (Hybrid)",
        "salary_range": "$85,000 - $115,000",
        "status": "open",
        "created_at": datetime.utcnow()
    },
    {
        "job_title": "Machine Learning Engineer",
        "description": "Join our AI team as a Machine Learning Engineer. You'll develop and deploy ML models, work with large datasets, and implement cutting-edge algorithms to solve complex problems.",
        "required_skills": "Python, TensorFlow, PyTorch, scikit-learn, Pandas, NumPy, Deep Learning, NLP, Computer Vision",
        "experience": "3-5 years",
        "location": "San Jose, CA (On-site)",
        "salary_range": "$140,000 - $180,000",
        "status": "open",
        "created_at": datetime.utcnow()
    },
    {
        "job_title": "UI/UX Designer",
        "description": "We're looking for a creative UI/UX Designer to design intuitive and engaging user interfaces. You'll conduct user research, create wireframes, and work with developers to bring designs to life.",
        "required_skills": "Figma, Adobe XD, Sketch, Prototyping, User Research, Wireframing, Visual Design, HTML/CSS",
        "experience": "3-5 years",
        "location": "Los Angeles, CA (Remote)",
        "salary_range": "$90,000 - $120,000",
        "status": "open",
        "created_at": datetime.utcnow()
    },
    {
        "job_title": "QA Automation Engineer",
        "description": "Seeking a QA Automation Engineer to design and implement automated testing frameworks. You'll ensure software quality through comprehensive test coverage and continuous testing.",
        "required_skills": "Selenium, Python, Java, TestNG, JUnit, API Testing, CI/CD, Git, Agile",
        "experience": "3-5 years",
        "location": "Chicago, IL (Hybrid)",
        "salary_range": "$95,000 - $125,000",
        "status": "open",
        "created_at": datetime.utcnow()
    },
    {
        "job_title": "Cloud Architect",
        "description": "We need an experienced Cloud Architect to design and implement scalable cloud solutions. You'll work with AWS/Azure services and lead cloud migration projects.",
        "required_skills": "AWS, Azure, Cloud Architecture, Microservices, Serverless, Security, Networking, Terraform",
        "experience": "7+ years",
        "location": "Dallas, TX (Remote)",
        "salary_range": "$150,000 - $200,000",
        "status": "open",
        "created_at": datetime.utcnow()
    },
    {
        "job_title": "Product Manager",
        "description": "Join us as a Product Manager to drive product strategy and roadmap. You'll work with cross-functional teams to deliver innovative products that meet customer needs.",
        "required_skills": "Product Strategy, Agile, Scrum, User Stories, Market Research, Analytics, Communication, Leadership",
        "experience": "5+ years",
        "location": "Denver, CO (Hybrid)",
        "salary_range": "$110,000 - $150,000",
        "status": "open",
        "created_at": datetime.utcnow()
    }
]

def insert_sample_jobs():
    """Insert sample jobs into the database."""
    try:
        # Connect to MongoDB
        client = MongoClient(Config.MONGO_URI)
        db = client[Config.DATABASE_NAME]
        jobs_collection = db['jobs']
        
        print("Connecting to MongoDB...")
        print(f"Connected to database: {Config.DATABASE_NAME}")
        
        # Check if jobs already exist
        existing_count = jobs_collection.count_documents({})
        print(f"\nCurrent jobs in database: {existing_count}")
        
        if existing_count > 0:
            response = input("\nJobs already exist. Do you want to add more? (yes/no): ")
            if response.lower() not in ['yes', 'y']:
                print("Operation cancelled.")
                return
        
        # Insert sample jobs
        print(f"\nInserting {len(SAMPLE_JOBS)} sample jobs...")
        result = jobs_collection.insert_many(SAMPLE_JOBS)
        
        print(f"Successfully inserted {len(result.inserted_ids)} jobs!")
        print("\nInserted Jobs:")
        print("-" * 80)
        
        for i, job in enumerate(SAMPLE_JOBS, 1):
            print(f"{i}. {job['job_title']}")
            print(f"   Location: {job['location']}")
            print(f"   Experience: {job['experience']}")
            print(f"   Salary: {job['salary_range']}")
            print()
        
        print("-" * 80)
        print(f"\nTotal jobs in database: {jobs_collection.count_documents({})}")
        print("\nSample jobs inserted successfully!")
        print("\nYou can now:")
        print("   1. View these jobs in the frontend")
        print("   2. Upload resumes to match against these jobs")
        print("   3. Test the AI matching functionality")
        
    except Exception as e:
        print(f"\nError inserting sample jobs: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()

if __name__ == "__main__":
    print("=" * 80)
    print("Sample Jobs Insertion Script")
    print("=" * 80)
    insert_sample_jobs()
