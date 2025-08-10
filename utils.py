import pdfplumber
import docx
import re
import spacy

# Load NLP model once (avoid repeated load for performance)
nlp = spacy.load("en_core_web_sm")

def extract_text_from_resume(file):
    """
    Extracts text content from a resume file (PDF or DOCX).
    Args:
        file (FileStorage): Uploaded resume file.
    Returns:
        str: Extracted text.
    """
    filename = file.filename.lower()

    try:
        if filename.endswith(".pdf"):
            with pdfplumber.open(file) as pdf:
                return "\n".join(page.extract_text() or "" for page in pdf.pages)

        elif filename.endswith(".docx"):
            doc = docx.Document(file)
            return "\n".join(para.text for para in doc.paragraphs)

        else:
            raise ValueError("Unsupported file type. Please upload a PDF or DOCX file.")

    except Exception as e:
        raise RuntimeError(f"Error extracting text from resume: {e}")


def parse_resume_data(text):
    """
    Parses essential details (email, phone, name, skills) from resume text.
    Args:
        text (str): Raw resume text.
    Returns:
        dict: Extracted structured data.
    """
    parsed_data = {}


    ]
    found_skills = [skill for skill in skills_list if skill.lower() in text.lower()]
    parsed_data["skills"] = ", ".join(found_skills)

    return parsed_data
