import fitz  # PyMuPDF
import docx2txt
import os

def extract_text(file_path):
    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        return None

def extract_text_from_pdf(file_path):
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
    except Exception as e:
        print("Error reading PDF:", e)
    return text

def extract_text_from_docx(file_path):
    try:
        text = docx2txt.process(file_path)
        return text
    except Exception as e:
        print("Error reading DOCX:", e)
        return ""