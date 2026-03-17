import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from endee import Endee, Precision

load_dotenv()

INDEX_NAME = "resume_jobs"
DIM = 384
_model = None
_client = None
_index = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def get_client():
    global _client
    if _client is None:
        auth = os.getenv("ENDEE_AUTH_TOKEN", "")
        _client = Endee(auth) if auth else Endee()
        url = os.getenv("ENDEE_URL", "")
        if url:
            _client.set_base_url(f"{url.rstrip('/')}/api/v1")
    return _client

def get_index():
    global _index
    if _index is None:
        client = get_client()
        existing = client.list_indexes()
        if INDEX_NAME not in existing:
            try:
                client.create_index(name=INDEX_NAME, dimension=DIM, space_type="cosine", precision=Precision.INT8)
            except Exception:
                pass
        _index = client.get_index(INDEX_NAME)
    return _index

def search(query, mode="jobs_for_resume", top_k=5):
    model = get_model()
    index = get_index()
    query_vector = model.encode([query])[0].tolist()
    fetch_k = top_k * 4 if mode != "all" else top_k
    raw_results = index.query(vector=query_vector, top_k=fetch_k)
    results = []
    for r in raw_results:
        rid = r["id"]
        similarity = r["similarity"]
        meta = r.get("meta", {})
        item_type = meta.get("type", "unknown")
        if mode == "jobs_for_resume" and item_type != "job":
            continue
        if mode == "resumes_for_job" and item_type != "resume":
            continue
        item = {
            "id": rid,
            "similarity": round(float(similarity) * 100, 1),
            "type": item_type,
        }
        item.update(meta)
        results.append(item)
        if len(results) >= top_k:
            break
    return results

def match_resume_to_jobs(resume_text, top_k=5):
    return search(resume_text, mode="jobs_for_resume", top_k=top_k)

def match_job_to_resumes(job_text, top_k=5):
    return search(job_text, mode="resumes_for_job", top_k=top_k)

def free_text_search(query, top_k=10):
    return search(query, mode="all", top_k=top_k)

def get_index_stats():
    try:
        client = get_client()
        index = client.get_index(INDEX_NAME)
        info = index.describe()
        return {
            "index_name": INDEX_NAME,
            "vector_count": info.get("count", 20),
            "dimension": DIM,
            "status": "connected",
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
