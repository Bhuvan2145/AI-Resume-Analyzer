from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2

app = Flask(__name__)
CORS(app)

skills_db = [
    "python",
    "java",
    "html",
    "css",
    "javascript",
    "react",
    "mongodb",
    "sql",
    "aws",
    "docker",
    "git",
    "nodejs",
    "spring boot",
    "flask",
    "machine learning",
    "data structures",
    "algorithms"
]

@app.route('/upload', methods=['POST'])
def upload_resume():

    file = request.files['resume']

    pdf_reader = PyPDF2.PdfReader(file)

    text = ""

    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    text = text.lower()

    found_skills = []

    for skill in skills_db:
        if skill in text:
            found_skills.append(skill)

    # Missing Skills
    missing_skills = []

    for skill in skills_db:
        if skill not in found_skills:
            missing_skills.append(skill)

    # ATS Score
    ats_score = len(found_skills) * 10

    # Job Recommendations
    jobs = []

    if "react" in found_skills:
        jobs.append("Frontend Developer")

    if "python" in found_skills:
        jobs.append("Python Developer")

    if "mongodb" in found_skills and "react" in found_skills:
        jobs.append("Full Stack Developer")

    return jsonify({
        "skills": found_skills,
        "missing_skills": missing_skills,
        "jobs": jobs,
        "ats_score": ats_score
    })

if __name__ == "__main__":
    app.run(debug=True)