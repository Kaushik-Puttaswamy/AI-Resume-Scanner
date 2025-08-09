from flask import Flask, render_template, request
from utils import extract_text_from_resume, parse_resume_data

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    parsed_data = {}

    if request.method == "POST":
        resume_file = request.files.get("resume")

        if not resume_file:
            return render_template("index.html", error="No file uploaded!")

        try:
            # Extract raw text from resume
            resume_text = extract_text_from_resume(resume_file)

            # Parse structured data from the text
            parsed_data = parse_resume_data(resume_text)

        except Exception as e:
            return render_template("index.html", error=f"Error processing file: {e}")

    return render_template("index.html", parsed_data=parsed_data)


if __name__ == "__main__":
    app.run(debug=True)
