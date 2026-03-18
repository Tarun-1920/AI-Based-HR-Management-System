"""
Test script for AI Resume Matcher module.

This script demonstrates how to use the calculate_match_score function
to compare resume text with job descriptions using TF-IDF and cosine similarity.
"""

from ai.resume_matcher import ResumeMatcher

def test_resume_matching():
    """Test resume matching with sample data."""
    
    # Initialize matcher
    matcher = ResumeMatcher()
    
    # Sample resume text
    resume_text = """
    John Doe
    Software Engineer
    
    EXPERIENCE:
    Senior Python Developer at Tech Corp (2020-2023)
    - Developed REST APIs using Flask and Django
    - Worked with MongoDB and PostgreSQL databases
    - Implemented machine learning models using scikit-learn
    - Deployed applications on AWS using Docker and Kubernetes
    - Collaborated with team using Git and Agile methodologies
    
    SKILLS:
    Python, Flask, Django, JavaScript, React, MongoDB, PostgreSQL, 
    AWS, Docker, Kubernetes, Machine Learning, Data Analysis, Git, 
    REST API, Agile, Scrum
    
    EDUCATION:
    Bachelor of Science in Computer Science
    """
    
    # Sample job description
    job_description = """
    Senior Python Developer
    
    We are looking for an experienced Python developer to join our team.
    
    REQUIREMENTS:
    - 3+ years of experience with Python
    - Strong knowledge of Flask or Django frameworks
    - Experience with MongoDB and SQL databases
    - Familiarity with AWS cloud services
    - Knowledge of Docker and Kubernetes
    - Experience with REST API development
    - Machine learning experience is a plus
    - Strong problem-solving and communication skills
    - Experience with Agile/Scrum methodologies
    
    REQUIRED SKILLS:
    Python, Flask, Django, MongoDB, AWS, Docker, Kubernetes, 
    REST API, Machine Learning, Agile, Git
    """
    
    print("=" * 70)
    print("AI RESUME MATCHER - TEST")
    print("=" * 70)
    print()
    
    # Test 1: Calculate match score
    print("TEST 1: Calculate Match Score")
    print("-" * 70)
    match_score = matcher.calculate_match_score(resume_text, job_description)
    print(f"Match Score: {match_score}%")
    print()
    
    # Test 2: Extract skills from resume
    print("TEST 2: Extract Skills from Resume")
    print("-" * 70)
    resume_skills = matcher.extract_skills(resume_text)
    print(f"Found {len(resume_skills)} skills:")
    print(", ".join(resume_skills))
    print()
    
    # Test 3: Extract skills from job description
    print("TEST 3: Extract Skills from Job Description")
    print("-" * 70)
    job_skills = matcher.extract_skills(job_description)
    print(f"Required {len(job_skills)} skills:")
    print(", ".join(job_skills))
    print()
    
    # Test 4: Detailed match analysis
    print("TEST 4: Detailed Match Analysis")
    print("-" * 70)
    analysis = matcher.get_detailed_match_analysis(resume_text, job_description)
    
    print(f"Overall Match Score: {analysis['overall_match_score']}%")
    print(f"Skills Match: {analysis['skills_match_percentage']}%")
    print(f"Total Resume Skills: {analysis['total_resume_skills']}")
    print(f"Total Required Skills: {analysis['total_required_skills']}")
    print(f"Matching Skills: {analysis['total_matching_skills']}")
    print()
    print(f"Matching Skills: {', '.join(analysis['matching_skills'])}")
    print()
    if analysis['missing_skills']:
        print(f"Missing Skills: {', '.join(analysis['missing_skills'])}")
    else:
        print("Missing Skills: None - Perfect match!")
    print()
    
    # Test 5: Low match example
    print("TEST 5: Low Match Example")
    print("-" * 70)
    
    unrelated_resume = """
    Jane Smith
    Marketing Manager
    
    EXPERIENCE:
    - Social media marketing
    - Content creation
    - Brand management
    - Customer engagement
    
    SKILLS:
    Marketing, Social Media, Content Writing, SEO, Google Analytics
    """
    
    low_match_score = matcher.calculate_match_score(unrelated_resume, job_description)
    print(f"Unrelated Resume Match Score: {low_match_score}%")
    print("(Expected to be low since marketing resume doesn't match tech job)")
    print()
    
    print("=" * 70)
    print("TESTS COMPLETED")
    print("=" * 70)

if __name__ == "__main__":
    test_resume_matching()
