from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from pathlib import Path
import os

from utils import extract_text_from_resume, parse_resume_data

# -----------------------------------------------------------------------------
# App Configuration
# -----------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "txt"}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB limit

app = Flask(__name__)
app.config.update(
    UPLOAD_FOLDER=str(UPLOAD_FOLDER),
    MAX_CONTENT_LENGTH=MAX_CONTENT_LENGTH,
    SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-key"),
)

UPLOAD_FOLDER.mkdir(exist_ok=True)


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def allowed_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    parsed_data = None

    if request.method == "POST":
        file = request.files.get("resume")

        if not file or file.filename == "":
            flash("Please select a resume file to upload.", "error")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Invalid file type. Allowed: PDF, DOC, DOCX, TXT.", "error")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        file_path = UPLOAD_FOLDER / filename

        try:
            file.save(file_path)

            resume_text = extract_text_from_resume(file_path)
            parsed_data = parse_resume_data(resume_text)

        except Exception as exc:
            app.logger.exception("Resume processing failed")
            flash(f"Error processing resume: {exc}", "error")

        finally:
            # Optional: clean up uploaded file
            if file_path.exists():
                file_path.unlink()

    return render_template("index.html", parsed_data=parsed_data)


# -----------------------------------------------------------------------------
# Error Handlers
# -----------------------------------------------------------------------------

@app.errorhandler(413)
def file_too_large(error):
    flash("File is too large. Maximum size is 5MB.", "error")
    return redirect(url_for("index"))


# -----------------------------------------------------------------------------
# Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
