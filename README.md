cd C:\Users\amili\OneDrive\Desktop\endee-resume-matcher
notepad README.md
```

Add at the top:
```
## 🎥 Demo Video
👉 Watch Demo: https://youtu.be/_Ui_5d4L0nE

# 🎯 AI Resume & Job Matching System — Endee Vector Database

A full-stack AI-powered **Resume and Job Matching System** built using **[Endee](https://github.com/endee-io/endee)** as the vector database. The system uses semantic similarity search to intelligently match candidates to jobs and jobs to candidates — going far beyond simple keyword matching.

---

## 🧠 Idea

Traditional job portals match resumes to jobs using keyword filters. This system uses **AI embeddings + vector similarity search** to understand the *meaning* of skills and experience, enabling:

- "Python Data Analyst with Power BI" → finds jobs requiring analytics + visualization
- A DevOps job description → finds candidates with cloud, Docker, CI/CD experience
- Even partial skill overlap is captured through semantic similarity

---

## 🏗️ System Design

```
┌──────────────────────────────────────────────────────────┐
│                    INGESTION PIPELINE                    │
│                                                          │
│  Resume / Job Text                                       │
│         │                                                │
│         ▼                                                │
│  all-MiniLM-L6-v2 → 384-dim embedding vector            │
│         │                                                │
│         ▼                                                │
│  ┌────────────────────────────────┐                      │
│  │      Endee Vector Database     │                      │
│  │   Index: resume_jobs           │                      │
│  │   Space: cosine, INT8          │                      │
│  │   Filter: {type: resume|job}   │  ← Endee filter API  │
│  └────────────────────────────────┘                      │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                     QUERY PIPELINE                       │
│                                                          │
│  User Query (text / resume / job description)            │
│         │                                                │
│         ▼                                                │
│  all-MiniLM-L6-v2 → query vector                        │
│         │                                                │
│         ▼                                                │
│  Endee index.query(vector, filter=[{type: job}])         │
│    → Top-K results by cosine similarity                  │
│         │                                                │
│         ▼                                                │
│  Results with similarity %, metadata → Web UI / API     │
└──────────────────────────────────────────────────────────┘
```

---

## 🔑 How Endee is Used

| Feature | Endee API Used |
|---|---|
| Store resume & job embeddings | `index.upsert([{id, vector, meta, filter}])` |
| Filter by type (resume or job) | `index.query(vector, filter=[{"type": {"$eq": "job"}}])` |
| Semantic similarity search | `index.query(vector, top_k=5)` |
| Check index status | `index.describe()` |
| Reset data | `client.delete_index(name)` |

**Endee's `filter` field** is used to separate resumes and jobs in a single index — enabling filtered queries like "search only jobs" or "search only resumes" with a single vector database.

---

## 🧰 Tech Stack

| Component | Tool |
|---|---|
| Vector Database | Endee (local Docker) |
| Embedding Model | `all-MiniLM-L6-v2` (384 dims, free, no API key) |
| Backend | Python Flask |
| Frontend | Pure HTML/CSS/JS (no framework needed) |
| PDF Parsing | PyPDF2 |
| Container | Docker Compose |

---

## 📁 Project Structure

```
endee-resume-matcher/
├── app.py              # Flask web server + API endpoints
├── search.py           # Semantic search logic (Endee queries)
├── data.py             # Seed data (10 resumes + 10 jobs) + ingestion script
├── docker-compose.yml  # Starts Endee on port 8080
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── README.md
└── templates/
    └── index.html      # Full web UI (4 tabs)
```

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.9+
- Docker and Docker Compose v2

### Step 1 — Clone your forked repo
```bash
git clone https://github.com/YOUR_USERNAME/endee-resume-matcher.git
cd endee-resume-matcher
```

### Step 2 — Start Endee
```bash
docker compose up -d
# Verify: curl http://localhost:8080/api/v1/index/list
```

### Step 3 — Install Python dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Configure environment
```bash
cp .env.example .env
# Default settings work out of the box. Edit only if needed.
```

### Step 5 — Ingest seed data into Endee
```bash
python data.py
# Ingests 10 resumes + 10 job descriptions into Endee
# To reset and re-ingest: python data.py --reset
```

### Step 6 — Run the web app
```bash
python app.py
# Open: http://localhost:5000
```

---

## 💬 Example Queries

| Query | Mode | Result |
|---|---|---|
| `Python Data Analyst with Power BI` | Jobs | Amazon Data Analyst, Deloitte BI Developer |
| `Machine Learning NLP deep learning` | Jobs | Google ML Engineer, Microsoft GenAI Engineer |
| `DevOps AWS Kubernetes CI/CD` | Jobs | Razorpay DevOps Engineer |
| Flipkart Senior Data Scientist JD | Resumes | Rahul Verma (Data Scientist), Priya Sharma |
| `NLP LLM RAG vector database` | Both | Deepika Iyer resume + Microsoft NLP job |

---

## 🌐 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `GET /` | GET | Web UI |
| `POST /api/search` | POST | Semantic search (text query) |
| `POST /api/upload_resume` | POST | Upload PDF resume, match to jobs |
| `GET /api/stats` | GET | Endee index statistics |

### POST /api/search
```json
{
  "query": "Python Data Analyst with Power BI",
  "mode": "jobs_for_resume",
  "top_k": 5
}
```

Modes: `jobs_for_resume`, `resumes_for_job`, `all`

---

## 📋 Mandatory Repository Steps

- ⭐ Starred [endee-io/endee](https://github.com/endee-io/endee)
- 🍴 Forked [endee-io/endee](https://github.com/endee-io/endee) to personal account
- This project is submitted as part of Tap Academy placement evaluation for Endee.io

---

## 📄 License

MIT License
