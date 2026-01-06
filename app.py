from flask import Flask, render_template, request
from utils import extract_text_from_resume, parse_resume_data
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "txt"}

# Create upload folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    parsed_data = {}

    if request.method == "POST":
        if "resume" not in request.files:
            return render_template("index.html", error="No file uploaded!")

        file = request.files["resume"]


        # Secure and save file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        try:
            # Extract and parse resume
            resume_text = extract_text_from_resume(file_path)
            parsed_data = parse_resume_data(resume_text)

        except Exception as e:
            return render_template(
                "index.html",
                error=f"Error processing resume: {str(e)}"
            )

    return render_template("index.html", parsed_data=parsed_data)


if __name__ == "__main__":
    app.run(debug=True)
