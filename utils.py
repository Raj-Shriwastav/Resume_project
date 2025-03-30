# intelligent_resume_analyzer_simple/utils.py
import os
from dotenv import load_dotenv
import streamlit as st

def load_api_key(api_name):
    """Loads the API key from Streamlit Secrets or environment variables."""
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]
    else:
        load_dotenv()
        api_key = os.getenv(api_name)
        if not api_key:
            raise ValueError(f"{api_name} API key not found in environment variables or Streamlit Secrets.")
        return api_key

def clean_text(text):
    """Cleans and normalizes the input text."""
    if not text:
        return ""
    text = text.lower()
    text = ''.join(char for char in text if char.isalnum() or char.isspace())
    text = ' '.join(text.split())
    return text