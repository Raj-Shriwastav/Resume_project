import streamlit as st
import google.generativeai as genai
import os
import PyPDF2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

def read_text_file(uploaded_file):
    return uploaded_file.read().decode("utf-8")

def read_pdf_file(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def generate_report_with_gemini(resume_text, job_description, model_name="models/gemini-2.0-flash"):
    """
    Generates a report by comparing a resume to a job description using Google's Gemini model.
    """
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel(model_name)
    prompt = f"""
    Analyze the following resume and job description.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Generate a report with the following sections:

    1. **Score based on key factors:** Provide a score (out of 100) indicating how well the resume matches the job description, considering the importance of different skills based on the role. Explain the weighting of key factors and the reasoning behind the score.

    2. **Most important skills to look out for:** List the essential skills mentioned in the job description that the user's resume seems to be lacking or could be strengthened.

    3. **Resume Score:** Provide an overall match score (out of 100) between the resume and the job description.

    4. **Project Score:** Evaluate the projects mentioned in the resume. Based on the job requirements, provide a score (out of 100) indicating how suitable the user's project experience is for this role. Explain your reasoning for the score.

    5. **Skill Score:** Based on the job description, scan the resume for relevant skills and provide a score (out of 100) indicating how well the resume demonstrates the required skills. Explain your reasoning.

    Format the report clearly with headings for each section and sub-points for explanations.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

st.title("Resume vs. Job Description Analyzer")

# Resume Input
st.subheader("Upload Resume")
resume_file = st.file_uploader("Choose a resume file (PDF or TXT)", type=["pdf", "txt"])
resume_text = ""
if resume_file is not None:
    file_type = resume_file.type
    if file_type == "application/pdf":
        resume_text = read_pdf_file(resume_file)
    elif file_type == "text/plain":
        resume_text = read_text_file(resume_file)
    else:
        st.error("Invalid resume file format. Please upload a PDF or TXT file.")

# Job Description Input
st.subheader("Enter Job Description")
job_desc_option = st.radio("How would you like to provide the job description?", ("Paste Text", "Upload File (PDF or TXT)"))
job_description = ""

if job_desc_option == "Paste Text":
    job_description = st.text_area("Paste the job description here:")
elif job_desc_option == "Upload File (PDF or TXT)":
    job_desc_file = st.file_uploader("Choose a job description file", type=["pdf", "txt"], key="job_desc_file")
    if job_desc_file is not None:
        file_type = job_desc_file.type
        if file_type == "application/pdf":
            job_description = read_pdf_file(job_desc_file)
        elif file_type == "text/plain":
            job_description = read_text_file(job_desc_file)
        else:
            st.error("Invalid job description file format. Please upload a PDF or TXT file.")

# Generate Report Button
if st.button("Generate Report"):
    if resume_text and job_description:
        if google_api_key:
            with st.spinner("Generating Report..."):
                report = generate_report_with_gemini(resume_text, job_description)
                st.subheader("Analysis Report")
                st.markdown(report)
        else:
            st.error("Please create a `.env` file in the same directory and add your Google API key as `GOOGLE_API_KEY=YOUR_API_KEY`.")
    else:
        st.warning("Please upload a resume and provide the job description.")