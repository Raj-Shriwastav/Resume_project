# intelligent_resume_analyzer_simple/ui.py
import streamlit as st

def display_header():
    """Displays the header of the application."""
    st.title("Intelligent Resume & Job Match Analyzer")
    st.markdown("Upload your resume and job description to get a detailed match analysis and suggestions.")
    st.markdown("---")

def upload_resume():
    """Allows the user to upload a resume file."""
    uploaded_file = st.file_uploader("Upload Resume (TXT, PDF)", type=["txt", "pdf"])
    return uploaded_file

def paste_job_description():
    """Allows the user to paste a job description."""
    job_description = st.text_area("Paste Job Description", height=200)
    return job_description

def display_analysis_button():
    """Displays the button to trigger the analysis."""
    analyze_button = st.button("Analyze")
    return analyze_button

def display_results_header():
    """Displays the header for the analysis results."""
    st.markdown("---")
    st.subheader("Analysis Results")

def display_score(overall_score, resume_score, skill_score, project_score):
    """Displays the overall and component scores."""
    st.metric("Overall Match Score", f"{overall_score:.2f}%")
    col1, col2, col3 = st.columns(3)
    col1.metric("Resume Score", f"{resume_score:.2f}%")
    col2.metric("Skill Score", f"{skill_score:.2f}%")
    col3.metric("Project Score", f"{project_score:.2f}%")
    st.markdown("---")

def display_skill_gap(skill_gaps):
    """Displays a bar chart of skill gaps."""
    if skill_gaps:
        st.subheader("Key Skill Gaps")
        st.bar_chart(skill_gaps)
    else:
        st.info("No significant skill gaps identified.")

def display_suggestions(suggested_projects, suggested_courses):
    """Displays suggestions for projects and courses."""
    if suggested_projects:
        st.subheader("Suggested Projects to Fill Gaps")
        for project in suggested_projects:
            st.markdown(f"- {project}")
        st.markdown("---")

    if suggested_courses:
        st.subheader("Suggested Courses to Learn Missing Skills")
        for course in suggested_courses:
            st.markdown(f"- {course}")
        st.markdown("---")

def display_important_skills(important_skills):
    """Displays the most important skills to look out for."""
    if important_skills:
        st.subheader("Most Important Skills to Look Out For")
        for skill in important_skills:
            st.markdown(f"- {skill}")
        st.markdown("---")

def display_project_score(project_score):
    """Displays the project score."""
    st.subheader("Project Score")
    st.metric("Project Score", f"{project_score:.2f}/100")
    st.markdown("---")

def display_skill_score_report(skill_score):
    """Displays the skill score."""
    st.subheader("Skill Score")
    st.metric("Skill Score", f"{skill_score:.2f}/100")
    st.markdown("---")

def display_mock_interview_links(mock_interview_links):
    """Displays links for mock interview preparation."""
    if mock_interview_links:
        st.subheader("Mock Interview Preparation Resources")
        for link in mock_interview_links:
            st.markdown(f"- {link}")
        st.markdown("---")
    else:
        st.info("No specific mock interview preparation resources found.")

def display_error(message):
    """Displays an error message."""
    st.error(message)

def display_info(message):
    """Displays an informational message."""
    st.info(message)