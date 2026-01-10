import re
import pdfplumber
import docx
import spacy
from typing import Dict

# Load spaCy model once
nlp = spacy.load("en_core_web_sm")


def extract_text_from_resume(file) -> str:
    """
    Extract text from PDF or DOCX resume.
    """
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        text = []
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        return "\n".join(text)

    elif filename.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join(para.text for para in doc.paragraphs if para.text.strip())

    return ""


def extract_email(text: str) -> str:
    match = re.search(r"\b[\w\.-]+@[\w\.-]+\.\w{2,}\b", text)
    return match.group(0) if match else ""


def extract_phone(text: str) -> str:
    match = re.search(
        r"(\+?\d{1,3}[\s-]?)?"
        r"(\(?\d{3}\)?[\s-]?)"
        r"\d{3}[\s-]?\d{4}",
        text
    )
    return match.group(0) if match else ""


def extract_name(text: str) -> str:
    """
    Extract candidate name using spaCy NER.
    Usually the first PERSON entity is the best guess.
    """
    doc = nlp(text[:1000])  # limit text for speed and accuracy

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

    return ""


def parse_resume_data(text: str) -> Dict[str, str]:
    """
    Parse structured data from resume text.
    """
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
    }
