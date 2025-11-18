from flask import Flask, render_template, request
from utils import extract_text_from_resume, parse_resume_data

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    parsed_data = {}
    if request.method == "POST":
        if 'resume' not in request.files:
            return render_template("index.html", error="No file uploaded!")
        file = request.files['resume']
        text = extract_text_from_resume(file)
        parsed_data = parse_resume_data(text)
    return render_template("index.html", parsed_data=parsed_data)

if __name__ == "__main__":
    app.run(debug=True)
