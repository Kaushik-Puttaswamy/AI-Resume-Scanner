import streamlit as st
from resume_parser import extract_text
from jd_matcher import compute_similarity
import tempfile

st.title("AI Resume Scanner (ATS-like)")

resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
jd_text = st.text_area("Paste Job Description")

if resume_file and jd_text:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(resume_file.read())
        tmp_path = tmp_file.name

    resume_text = extract_text(tmp_path)
    if resume_text:
        score = compute_similarity(resume_text, jd_text)
        st.success(f"Resume Match Score: {score * 100:.2f}%")
    else:
        st.error("Failed to extract text from the uploaded resume.")