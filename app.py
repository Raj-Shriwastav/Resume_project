# intelligent_resume_analyzer_simple/app.py
import streamlit as st
from ui import (
    display_header,
    upload_resume,
    paste_job_description,
    display_analysis_button,
    display_results_header,
    display_score,
    display_skill_gap,
    display_suggestions,
    display_important_skills,
    display_project_score,
    display_skill_score_report,
    display_mock_interview_links,
    display_error,
    display_info,
)
from preprocessing import extract_text_from_file, preprocess_text
from llm_integration import LLMClient
from scoring import normalize_score
import pandas as pd

def main():
    display_header()

    resume_file = upload_resume()
    job_description_text = paste_job_description()

    if display_analysis_button():
        if resume_file is None:
            display_error("Please upload your resume.")
            return
        if not job_description_text:
            display_error("Please paste the job description.")
            return

        with st.spinner("Analyzing..."):
            try:
                resume_text_raw = extract_text_from_file(resume_file)
                if resume_text_raw is None:
                    display_error("Could not extract text from the resume. Please ensure it's a valid TXT or PDF file.")
                    return
                resume_text_processed = preprocess_text(resume_text_raw)
                job_description_processed = preprocess_text(job_description_text)

                try:
                    llm_client = LLMClient()
                    llm_response = llm_client.analyze_resume_job_match(resume_text_processed, job_description_processed)
                except ImportError as e:
                    display_error(f"Error initializing LLM: {e}")
                    display_info("Please ensure you have installed the google-generativeai library and set up your API key in a .env file.")
                    return

                if llm_response:
                    overall_match_score = normalize_score(llm_response.get("overall_match_score", 0.0))
                    resume_score = normalize_score(llm_response.get("resume_score", 0.0))
                    skill_score = normalize_score(llm_response.get("skill_score", 0.0))
                    project_score = normalize_score(llm_response.get("project_score", 0.0))
                    key_skill_gaps = llm_response.get("key_skill_gaps", [])
                    suggested_projects = llm_response.get("suggested_projects", [])
                    suggested_courses = llm_response.get("suggested_courses", [])
                    important_skills = llm_response.get("important_skills", [])
                    mock_interview_links = llm_response.get("mock_interview_links", [])

                    display_results_header()
                    display_score(overall_match_score, resume_score, skill_score, project_score)

                    display_important_skills(important_skills)
                    display_project_score(project_score)
                    display_skill_score_report(skill_score)

                    if key_skill_gaps:
                        skill_gap_counts = pd.Series(key_skill_gaps).value_counts()
                        st.subheader("Key Skill Gaps")
                        st.bar_chart(skill_gap_counts)

                    display_suggestions(suggested_projects, suggested_courses)
                    display_mock_interview_links(mock_interview_links)

                else:
                    display_error("Failed to get a valid response from the LLM.")

            except Exception as e:
                display_error(f"An error occurred during analysis: {e}")

if __name__ == "__main__":
    main()