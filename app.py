
from flask import Flask, request, jsonify
import mysql.connector
import os
from config import DB_CONFIG

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# DATABASE 

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_latest_resume_text():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT resume_text FROM resumes ORDER BY id DESC LIMIT 1"
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None


def get_all_resumes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, resume_text FROM resumes")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


# UPLOAD CONFIG 

UPLOAD_FOLDER = 'data'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ROUTES 

@app.route("/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE();")
    db_name = cursor.fetchone()
    cursor.close()
    conn.close()
    return f"Connected to database: {db_name[0]}"

@app.route("/upload", methods=["POST"])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['resume']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # READ RESUME TEXT
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            resume_text = f.read()

        # SAVE TO DATABASE
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO resumes (resume_text) VALUES (%s)",
            (resume_text,)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Resume uploaded & saved to DB"}), 200

    return jsonify({"error": "File type not allowed"}), 400



@app.route("/match", methods=["POST"])
def match_resume():
    data = request.get_json()

    if not data or "job_description" not in data:
        return jsonify({"error": "Job description required"}), 400

    resume_text = get_latest_resume_text()

    if not resume_text:
        return jsonify({"error": "No resume found"}), 404

    job_desc = data["job_description"]

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, job_desc])

    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    match_percentage = round(score * 100, 2)

    return jsonify({
        "match_percentage": match_percentage
    }), 200

@app.route("/rank", methods=["POST"])
def rank_resumes():
    data = request.get_json()

    if not data or "job_description" not in data:
        return jsonify({"error": "Job description required"}), 400

    job_desc = data["job_description"]
    resumes = get_all_resumes()

    if not resumes:
        return jsonify({"error": "No resumes found"}), 404

    texts = [r[1] for r in resumes]
    texts.append(job_desc)

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(texts)

    job_vector = vectors[-1]
    resume_vectors = vectors[:-1]

    scores = cosine_similarity(resume_vectors, job_vector).flatten()

    ranked = []
    for i, score in enumerate(scores):
        ranked.append({
            "resume_id": resumes[i][0],
            "match_percentage": round(score * 100, 2)
        })

    ranked = sorted(ranked, key=lambda x: x["match_percentage"], reverse=True)

    return jsonify(ranked), 200


# MAIN

if __name__ == "__main__":
    app.run(debug=True)
