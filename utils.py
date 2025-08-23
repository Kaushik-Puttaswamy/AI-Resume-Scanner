import pdfplumber
import docx
import re
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_resume(file):
    if file.filename.endswith('.pdf'):
        with pdfplumber.open(file) as pdf:
            return '\n'.join(page.extract_text() or '' for page in pdf.pages)
    elif file.filename.endswith('.docx'):
        doc = docx.Document(file)
        return '\n'.join([para.text for para in doc.paragraphs])
    else:
        return ""

