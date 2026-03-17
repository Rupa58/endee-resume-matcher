import os
import json
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

def call_gemini(prompt):
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return "GEMINI_API_KEY not set in .env file."
    url = f"{GEMINI_API_URL}?key={api_key}"
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 600}
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except urllib.error.HTTPError as e:
        return f"Gemini API error {e.code}: {e.read().decode('utf-8')[:200]}"
    except Exception as e:
        return f"Error calling Gemini: {str(e)}"

def explain_resume_job_match(resume, job):
    prompt = f"""You are an expert HR recruiter and career coach.
Analyze the match between this candidate and job. Respond in JSON format only.

CANDIDATE PROFILE:
- Name: {resume.get("name", "Candidate")}
- Title: {resume.get("title", "")}
- Skills: {resume.get("skills", "")}
- Experience: {resume.get("experience", "")}
- Education: {resume.get("education", "")}
- Summary: {resume.get("summary", "")}

JOB OPENING:
- Title: {job.get("title", "")}
- Company: {job.get("company", "")}
- Required Skills: {job.get("required_skills", "")}
- Responsibilities: {job.get("responsibilities", "")}
- Description: {job.get("description", "")}
- Experience Required: {job.get("experience_required", "")}

Respond with ONLY this JSON (no markdown, no extra text):
{{
  "match_score_explanation": "2-3 sentences explaining why this candidate matches this job",
  "strengths": ["strength 1", "strength 2", "strength 3"],
  "gaps": ["gap 1 or None if no gaps"],
  "interview_questions": [
    "Question 1 based on their experience?",
    "Question 2 about their technical skills?",
    "Question 3 about a specific project?",
    "Question 4 about a skill gap or growth area?",
    "Question 5 about their career goals?"
  ]
}}"""
    response = call_gemini(prompt)
    try:
        clean = response.strip()
        if clean.startswith("`"):
            clean = clean.split("`")[1]
            if clean.startswith("json"):
                clean = clean[4:]
        return json.loads(clean.strip())
    except Exception:
        return {
            "match_score_explanation": response,
            "strengths": [],
            "gaps": [],
            "interview_questions": []
        }
