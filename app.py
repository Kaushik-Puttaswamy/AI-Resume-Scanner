from flask import Flask, render_template, request, redirect, url_for
from utils import extract_text_from_resume, parse_resume_data
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Optional: restrict upload types
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "txt"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    parsed_data = {}

    if request.method == "POST":
        if "resume" not in request.files:
            return render_template("index.html", error="No file uploaded!")

        file = request.files["resume"]

        if file.filename == "":
            return render_template("index.html", error="No file selected!")

        if not allowed_file(file.filename):
            return render_template("index.html", error="Unsupported file type!")

        filename = secure_filename(file.filename)

        try:
            # Extract raw text from resume
            text = extract_text_from_resume(file)

            if not text.strip():
                return render_template("index.html", error="Unable to extract text from file.")


if __name__ == "__main__":
    app.run(debug=True)
