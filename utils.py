import pdfplumber
import docx
import re
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_resume(file):
    """Extracts and cleans text from PDF or DOCX resumes."""
    text = ""

    if file.filename.endswith('.pdf'):
        with pdfplumber.open(file) as pdf:
            text = "\n".join(page.extract_text() or '' for page in pdf.pages)
    elif file.filename.endswith('.docx'):
        doc = docx.Document(file)
        text = "\n".join(para.text for para in doc.paragraphs)
    else:
        return ""

    # Basic cleaning
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def parse_resume_data(text):
    """Parses key information like name, email, phone, and skills."""
    parsed_data = {}

    # --- Email ---
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    email = re.search(email_pattern, text)
    parsed_data["email"] = email.group(0) if email else ""

    # --- Phone ---
    phone_pattern = r'(\+?\d{1,3}[\s-]?)?(\(?\d{3}\)?[\s-]?)?\d{3}[\s-]?\d{4}'
    phone = re.search(phone_pattern, text)
    parsed_data["phone"] = phone.group(0) if phone else ""

    # --- Name ---
    doc = nlp(text)
    name = ""
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text.strip()
            break

    # Fallback: use first line if spaCy fails
    if not name:
        first_line = text.split('\n')[0]
        if len(first_line.split()) <= 5:
            name = first_line.strip()

    parsed_data["name"] = name

    # --- Optional: Skills Extraction ---
    skills_keywords = [
        "Python", "Java", "C++", "SQL", "Excel", "Machine Learning", "Data Analysis",
        "AWS", "JavaScript", "HTML", "CSS", "Django", "Flask", "React", "TensorFlow",
        "Leadership", "Communication", "Project Management"
    ]

    found_skills = [skill for skill in skills_keywords if re.search(rf'\b{skill}\b', text, re.IGNORECASE)]
    parsed_data["skills"] = list(set(found_skills))

    # --- Optional: Education Extraction ---
    education_pattern = r'\b(Bachelor|Master|MBA|B\.Tech|M\.Tech|Ph\.D|BSc|MSc)[^.,;\n]*'
    education = re.findall(education_pattern, text, re.IGNORECASE)
    parsed_data["education"] = list(set(education))

    # --- Optional: Experience Section ---
    exp_pattern = r'(?i)(experience|employment history|work history)[:\n-]?(.*?)\n\n'
    experience = re.findall(exp_pattern, text)
    parsed_data["experience"] = experience[0][1].strip() if experience else ""

    return parsed_data
