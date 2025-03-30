# intelligent_resume_analyzer_simple/preprocessing.py
import io
from pdfminer.high_level import extract_text_to_fp
import nltk
from nltk.corpus import stopwords
from utils import clean_text

nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))

def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF file."""
    try:
        output_string = io.StringIO()
        extract_text_to_fp(pdf_file, output_string)
        return output_string.getvalue()
    except Exception as e:
        raise Exception(f"Error during PDF text extraction: {e}. Ensure the PDF is text-based.")

def extract_text_from_file(uploaded_file):
    """Extracts text from the uploaded file based on its type."""
    if uploaded_file is not None:
        file_name = uploaded_file.name
        if file_name.endswith(".txt"):
            return uploaded_file.read().decode("utf-8")
        elif file_name.endswith(".pdf"):
            return extract_text_from_pdf(uploaded_file)
    return None

def preprocess_text(text):
    """Preprocesses the input text by cleaning and removing stop words."""
    if not text:
        return ""
    cleaned_text = clean_text(text)
    words = cleaned_text.split()
    filtered_words = [word for word in words if word not in stop_words]
    return " ".join(filtered_words)