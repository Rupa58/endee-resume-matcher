import os
import io
import json
import PyPDF2
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from search import match_resume_to_jobs, match_job_to_resumes, free_text_search, get_index_stats
from rag import explain_resume_job_match

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
MAX_UPLOAD_BYTES = 5 * 1024 * 1024

def extract_pdf_text(file_bytes):
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    return " ".join(page.extract_text() or "" for page in reader.pages).strip()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/search", methods=["POST"])
def api_search():
    data = request.get_json(force=True, silent=True) or {}
    query = (data.get("query") or "").strip()
    mode = data.get("mode", "jobs_for_resume")
    top_k = min(int(data.get("top_k", 5)), 10)
    if not query:
        return jsonify({"error": "Query is required."}), 400
    if mode not in ("jobs_for_resume", "resumes_for_job", "all"):
        return jsonify({"error": "Invalid mode."}), 400
    try:
        if mode == "jobs_for_resume":
            results = match_resume_to_jobs(query, top_k=top_k)
        elif mode == "resumes_for_job":
            results = match_job_to_resumes(query, top_k=top_k)
        else:
            results = free_text_search(query, top_k=top_k)
        return jsonify({"results": results, "count": len(results)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/rag_explain", methods=["POST"])
def api_rag_explain():
    data = request.get_json(force=True, silent=True) or {}
    resume = data.get("resume", {})
    job = data.get("job", {})
    if not resume or not job:
        return jsonify({"error": "Both resume and job are required."}), 400
    try:
        result = explain_resume_job_match(resume, job)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/upload_resume", methods=["POST"])
def api_upload_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded."}), 400
    f = request.files["resume"]
    if not f.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported."}), 400
    raw = f.read(MAX_UPLOAD_BYTES)
    try:
        text = extract_pdf_text(raw)
    except Exception as e:
        return jsonify({"error": f"Could not read PDF: {e}"}), 400
    if len(text) < 30:
        return jsonify({"error": "PDF appears to be empty or unreadable."}), 400
    top_k = int(request.form.get("top_k", 5))
    try:
        results = match_resume_to_jobs(text, top_k=top_k)
        return jsonify({"extracted_text": text[:400] + "...", "results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/stats")
def api_stats():
    return jsonify(get_index_stats())

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"\n🚀 Starting AI Resume Matcher + RAG on http://localhost:{port}")
    app.run(debug=True, host="0.0.0.0", port=port)
