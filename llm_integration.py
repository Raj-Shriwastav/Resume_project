# intelligent_resume_analyzer_simple/llm_integration.py
from utils import load_api_key
import json

class LLMClient:
    def __init__(self):
        try:
            import google.generativeai as genai
            self.api_key = load_api_key("GEMINI_API_KEY")
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('models/gemini-2.0-flash')
        except ImportError:
            raise ImportError("Please install the google-generativeai library.")

    def analyze_resume_job_match(self, resume_text, job_description):
        """Analyzes the resume and job description using Gemini."""
        prompt = f"""Analyze the following resume and job description to determine the match.

Based on the job description, identify the most important skills and assign weights to different skills and experiences based on their relevance to the role. For example, UI/UX skills should be weighted higher for a Front End Developer role than Python skills, even if both are mentioned.

Generate a report containing the following as a JSON object:

- "overall_match_score": (float, percentage score reflecting the overall suitability)
- "resume_score": (float, percentage score based on the overall content and relevance of the resume to the job description)
- "skill_score": (integer, score out of 100 representing how well the user's skills match the job requirements, based on both explicitly listed skills and skills demonstrated in their experience)
- "project_score": (integer, score out of 100 evaluating the relevance and suitability of the user's projects to the job requirements)
- "important_skills": (list of the most critical skills the user should possess for this role)
- "key_skill_gaps": (list of skills mentioned in the job description that are not prominent or evident in the resume)
- "suggested_projects": (list of project ideas with a brief description or a link to a relevant GitHub project that the user can undertake to learn and showcase the missing important skills. The project level should be appropriate for the job description)
- "suggested_courses": (list of relevant online courses from platforms like Coursera, Udemy, edX, etc., that can help the user learn the missing important skills)
- "mock_interview_links": (list of relevant links to websites or resources that offer mock interview preparation for this type of role and potentially for specific companies)

Resume:
{resume_text}

Job Description:
{job_description}
"""
        try:
            response = self.model.generate_content(prompt)
            if response and response.parts:
                raw_text = response.parts[0].text
                print("Raw Gemini Response Text:", raw_text)  # For debugging

                cleaned_text = raw_text.strip()
                if cleaned_text.startswith("```json"):
                    cleaned_text = cleaned_text[len("```json"):].strip()
                if cleaned_text.endswith("```"):
                    cleaned_text = cleaned_text[:-len("```")].strip()

                try:
                    return json.loads(cleaned_text)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from Gemini after cleaning: {e}")
                    print(f"Problematic JSON String after cleaning: {cleaned_text}")
                    return None
            else:
                print("No response or empty parts from Gemini.")
                return None
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return None