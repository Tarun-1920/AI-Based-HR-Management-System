from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import numpy as np

class ResumeMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            lowercase=True,
            max_features=1000,
            ngram_range=(1, 2)  # Use unigrams and bigrams
        )
        
        self.common_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node',
            'sql', 'mongodb', 'postgresql', 'mysql', 'aws', 'azure', 'gcp',
            'docker', 'kubernetes', 'git', 'jenkins', 'ci/cd', 'devops',
            'machine learning', 'deep learning', 'data analysis', 'data science',
            'artificial intelligence', 'nlp', 'computer vision', 'tensorflow',
            'pytorch', 'scikit-learn', 'pandas', 'numpy', 'flask', 'django',
            'spring boot', 'rest api', 'graphql', 'microservices', 'agile',
            'scrum', 'leadership', 'communication', 'problem solving', 'teamwork',
            'html', 'css', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go',
            'swift', 'kotlin', 'scala', 'rust', 'redis', 'elasticsearch',
            'kafka', 'rabbitmq', 'linux', 'unix', 'windows', 'networking'
        ]

    def calculate_match_score(self, resume_text, job_description):
        """
        Calculate match score between resume and job description using TF-IDF and cosine similarity.
        
        Args:
            resume_text (str): Text extracted from candidate's resume
            job_description (str): Job requirements and description
            
        Returns:
            float: Match score as percentage (0-100)
        """
        
        # Validate inputs
        if not resume_text or not job_description:
            return 0.0
        
        # Clean and preprocess text
        resume_clean = self._preprocess_text(resume_text)
        job_clean = self._preprocess_text(job_description)
        
        if not resume_clean or not job_clean:
            return 0.0
        
        try:
            # Create TF-IDF vectors
            documents = [resume_clean, job_clean]
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            
            # Calculate cosine similarity
            # tfidf_matrix[0] = resume vector
            # tfidf_matrix[1] = job description vector
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Convert to percentage and round to 2 decimal places
            match_score = round(similarity * 100, 2)
            
            # Ensure score is between 0 and 100
            match_score = max(0.0, min(100.0, match_score))
            
            return match_score
            
        except Exception as e:
            print(f"Error calculating match score: {str(e)}")
            return 0.0

    def _preprocess_text(self, text):
        """
        Preprocess text by removing special characters and extra whitespace.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep alphanumeric and spaces
        text = re.sub(r'[^a-z0-9\s+#]', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text

    def extract_skills(self, resume_text):
        """
        Extract skills from resume text by matching against common skills list.
        
        Args:
            resume_text (str): Text extracted from resume
            
        Returns:
            list: List of found skills
        """
        if not resume_text:
            return []
        
        resume_lower = resume_text.lower()
        found_skills = []
        
        # Search for each skill in the resume
        for skill in self.common_skills:
            # Use word boundaries to match whole words/phrases
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, resume_lower):
                found_skills.append(skill)
        
        # Remove duplicates and sort
        found_skills = sorted(list(set(found_skills)))
        
        return found_skills

    def get_detailed_match_analysis(self, resume_text, job_description):
        """
        Get detailed analysis of resume-job match including skills overlap.
        
        Args:
            resume_text (str): Text extracted from candidate's resume
            job_description (str): Job requirements and description
            
        Returns:
            dict: Detailed match analysis
        """
        
        # Calculate overall match score
        match_score = self.calculate_match_score(resume_text, job_description)
        
        # Extract skills from both
        resume_skills = self.extract_skills(resume_text)
        job_skills = self.extract_skills(job_description)
        
        # Find matching and missing skills
        matching_skills = list(set(resume_skills) & set(job_skills))
        missing_skills = list(set(job_skills) - set(resume_skills))
        
        # Calculate skills match percentage
        skills_match = 0.0
        if job_skills:
            skills_match = round((len(matching_skills) / len(job_skills)) * 100, 2)
        
        return {
            'overall_match_score': match_score,
            'skills_match_percentage': skills_match,
            'resume_skills': resume_skills,
            'job_required_skills': job_skills,
            'matching_skills': matching_skills,
            'missing_skills': missing_skills,
            'total_resume_skills': len(resume_skills),
            'total_required_skills': len(job_skills),
            'total_matching_skills': len(matching_skills)
        }
