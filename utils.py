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

def parse_resume_data(text):
    parsed_data = {}
    # Extract email
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    parsed_data["email"] = email.group(0) if email else ""
    # Extract phone number
    phone = re.search(r'(\+?\d{1,4}[\s-])?(?:\d{10}|\d{3}[\s-]\d{3}[\s-]\d{4})', text)
    parsed_data["phone"] = phone.group(0) if phone else ""
    # Extract name (using spaCy for better accuracy)
    doc = nlp(text)
    name = ""
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break
    parsed_data["name"] = name

