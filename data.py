import sys, os
from dotenv import load_dotenv
load_dotenv()

RESUMES = [
    {"id":"resume_001","name":"Priya Sharma","title":"Data Analyst","skills":"Python, SQL, Power BI, Excel, Tableau, Pandas, Statistics","experience":"3 years at TCS. Built Power BI dashboards. Wrote SQL queries. Used Python and Pandas.","education":"B.Tech Computer Science, VIT University 2020","location":"Bangalore","summary":"Data Analyst skilled in Python, SQL, and Power BI."},
    {"id":"resume_002","name":"Arjun Mehta","title":"Machine Learning Engineer","skills":"Python, TensorFlow, PyTorch, Deep Learning, NLP, BERT, Docker, AWS, MLOps","experience":"4 years at Infosys. Built NLP models. Deployed ML models on AWS SageMaker.","education":"M.Tech AI, IIT Hyderabad 2019","location":"Hyderabad","summary":"ML Engineer with 4 years in deep learning and NLP."},
    {"id":"resume_003","name":"Sneha Reddy","title":"Full Stack Developer","skills":"React, Node.js, JavaScript, TypeScript, MongoDB, REST APIs, Docker","experience":"2 years at Wipro. Built web apps with React and Node.js. Designed REST APIs.","education":"B.E. CSE, Osmania University 2021","location":"Hyderabad","summary":"Full Stack Developer with 2 years in React and Node.js."},
    {"id":"resume_004","name":"Rahul Verma","title":"Data Scientist","skills":"Python, Machine Learning, Statistics, SQL, A/B Testing, Scikit-learn, Recommendation Systems","experience":"5 years at Flipkart. Built recommendation engine. Conducted A/B tests.","education":"M.Sc Statistics, Delhi University 2018","location":"Delhi","summary":"Senior Data Scientist with 5 years at Flipkart."},
    {"id":"resume_005","name":"Kavya Nair","title":"DevOps Engineer","skills":"AWS, Docker, Kubernetes, Terraform, CI/CD, Jenkins, Linux, Ansible","experience":"3 years at Accenture. Built CI/CD pipelines. Managed Kubernetes on AWS EKS.","education":"B.Tech IT, BITS Pilani 2020","location":"Pune","summary":"DevOps Engineer with 3 years in AWS and Kubernetes."},
    {"id":"resume_006","name":"Aman Gupta","title":"BI Analyst","skills":"Power BI, Tableau, SQL, Excel, DAX, ETL, Data Warehousing","experience":"4 years at Deloitte. Created Power BI dashboards. Built ETL pipelines.","education":"MBA Analytics, ISB Hyderabad 2019","location":"Gurgaon","summary":"BI Analyst expert in Power BI, Tableau, and SQL."},
    {"id":"resume_007","name":"Deepika Iyer","title":"NLP Engineer","skills":"Python, NLP, Hugging Face, BERT, GPT, LLM, LangChain, RAG, Vector Databases","experience":"3 years at Amazon. Fine-tuned BERT. Built RAG chatbot with LangChain.","education":"M.Tech CSE, IIT Madras 2021","location":"Chennai","summary":"NLP Engineer expert in LLMs, BERT, and RAG pipelines."},
    {"id":"resume_008","name":"Vikram Singh","title":"Android Developer","skills":"Android, Kotlin, MVVM, Jetpack Compose, REST APIs, Firebase","experience":"3 years at Paytm. Built payment features for 10M users. Migrated Java to Kotlin.","education":"B.Tech CSE, Pune University 2020","location":"Noida","summary":"Android Developer expert in Kotlin and Jetpack Compose."},
    {"id":"resume_009","name":"Ananya Bose","title":"Data Engineer","skills":"Python, Apache Spark, Kafka, Airflow, Snowflake, dbt, AWS, ETL","experience":"4 years at Zomato. Built real-time Kafka and Spark pipelines. Used Airflow.","education":"B.Tech CSE, NIT Warangal 2019","location":"Bangalore","summary":"Data Engineer with 4 years at Zomato building real-time pipelines."},
    {"id":"resume_010","name":"Rohan Joshi","title":"AI/ML Fresher","skills":"Python, Machine Learning, Scikit-learn, Pandas, NumPy, SQL, Jupyter","experience":"6-month internship. Built sentiment analysis model. Top 10% on Kaggle.","education":"B.Tech CSE Final Year, BITS Goa 2025","location":"Bangalore","summary":"Final year student passionate about AI/ML. Active Kaggle competitor."},
]

JOBS = [
    {"id":"job_001","title":"Data Analyst","company":"Amazon India","location":"Bangalore","required_skills":"Python, SQL, Power BI, Excel, Tableau, Statistics","responsibilities":"Build Power BI dashboards. Write SQL queries. Present insights.","description":"Looking for Data Analyst to build dashboards and help make data-driven decisions.","experience_required":"2-4 years"},
    {"id":"job_002","title":"Machine Learning Engineer","company":"Google India","location":"Hyderabad","required_skills":"Python, TensorFlow, PyTorch, NLP, Deep Learning, MLOps, Docker, AWS","responsibilities":"Train deep learning models. Deploy ML to production. Build MLOps pipelines.","description":"Join Google AI to build world-class ML systems at scale.","experience_required":"3-6 years"},
    {"id":"job_003","title":"Full Stack Engineer","company":"Swiggy","location":"Bangalore","required_skills":"React, Node.js, JavaScript, TypeScript, MongoDB, REST APIs, Docker","responsibilities":"Build web applications. Design REST APIs. Optimize performance.","description":"Swiggy hiring Full Stack Engineer for features used by millions daily.","experience_required":"2-5 years"},
    {"id":"job_004","title":"Senior Data Scientist","company":"Flipkart","location":"Bangalore","required_skills":"Python, Machine Learning, Statistics, SQL, A/B Testing, Recommendation Systems","responsibilities":"Lead data science projects. Build recommendation models. Run A/B tests.","description":"Senior Data Scientist for Flipkart personalization impacting 100M+ users.","experience_required":"4-8 years"},
    {"id":"job_005","title":"DevOps Engineer","company":"Razorpay","location":"Bangalore","required_skills":"AWS, Docker, Kubernetes, Terraform, CI/CD, Jenkins, Linux","responsibilities":"Manage AWS infrastructure. Build CI/CD pipelines. Infrastructure as code.","description":"Razorpay hiring DevOps Engineer for cloud-native payment infrastructure.","experience_required":"2-5 years"},
    {"id":"job_006","title":"Power BI Developer","company":"Deloitte India","location":"Gurgaon","required_skills":"Power BI, SQL, DAX, Excel, Data Warehousing, ETL, Tableau","responsibilities":"Develop Power BI reports. Design data models. Write DAX measures.","description":"Deloitte hiring BI Developer for Fortune 500 analytics solutions.","experience_required":"3-6 years"},
    {"id":"job_007","title":"NLP and GenAI Engineer","company":"Microsoft India","location":"Hyderabad","required_skills":"Python, NLP, LLM, Hugging Face, LangChain, RAG, Vector Databases, BERT","responsibilities":"Build LLM apps and RAG pipelines. Fine-tune models. Integrate vector search.","description":"Microsoft hiring NLP GenAI engineer for AI products using LLMs and RAG.","experience_required":"2-5 years"},
    {"id":"job_008","title":"Android Developer","company":"PhonePe","location":"Bangalore","required_skills":"Android, Kotlin, MVVM, Jetpack Compose, REST APIs, Firebase","responsibilities":"Build Android features. Write Kotlin code. Optimize app performance.","description":"PhonePe hiring Android Developer for India largest fintech app 400M users.","experience_required":"2-4 years"},
    {"id":"job_009","title":"Data Engineer","company":"Ola","location":"Bangalore","required_skills":"Python, Apache Spark, Kafka, Airflow, Snowflake, dbt, AWS","responsibilities":"Build real-time data pipelines. Design Snowflake models. Set up Airflow DAGs.","description":"Ola hiring Data Engineer for analytics infrastructure powering 1M daily rides.","experience_required":"3-6 years"},
    {"id":"job_010","title":"Junior Data Scientist","company":"BuildFast AI","location":"Remote","required_skills":"Python, Machine Learning, Scikit-learn, Pandas, SQL","responsibilities":"Build ML models. Data preprocessing. Run experiments.","description":"BuildFast AI hiring Junior Data Scientist. Freshers welcome.","experience_required":"0-1 years"},
]

def build_resume_text(r):
    return f"Name: {r['name']}. Title: {r['title']}. Skills: {r['skills']}. Experience: {r['experience']}. Education: {r['education']}. Summary: {r['summary']}"

def build_job_text(j):
    return f"Job Title: {j['title']}. Company: {j['company']}. Required Skills: {j['required_skills']}. Responsibilities: {j['responsibilities']}. Description: {j['description']}"

def ingest_all(reset=False):
    from sentence_transformers import SentenceTransformer
    from endee import Endee, Precision
    INDEX_NAME = "resume_jobs"
    DIM = 384
    print("\n🔌 Connecting to Endee...")
    auth = os.getenv("ENDEE_AUTH_TOKEN", "")
    client = Endee(auth) if auth else Endee()
    url = os.getenv("ENDEE_URL", "")
    if url:
        client.set_base_url(f"{url.rstrip('/')}/api/v1")
    if reset:
        try:
            client.delete_index(INDEX_NAME)
            print("🗑️  Old index deleted.")
        except Exception:
            pass
    existing = client.list_indexes()
    if INDEX_NAME not in existing:
        try:
            client.create_index(name=INDEX_NAME, dimension=DIM, space_type="cosine", precision=Precision.INT8)
        except Exception:
            pass
        print(f"✅ Created Endee index: '{INDEX_NAME}'")
    else:
        print(f"ℹ️  Index '{INDEX_NAME}' already exists.")
    index = client.get_index(INDEX_NAME)
    print("\n📦 Loading sentence-transformer model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ Model loaded.\n")
    print(f"👤 Ingesting {len(RESUMES)} resumes...")
    resume_texts = [build_resume_text(r) for r in RESUMES]
    resume_embeddings = model.encode(resume_texts, show_progress_bar=False)
    resume_vectors = []
    for r, emb in zip(RESUMES, resume_embeddings):
        resume_vectors.append({"id": r["id"], "vector": emb.tolist(), "meta": {"type": "resume", "name": r["name"], "title": r["title"], "skills": r["skills"], "experience": r["experience"], "education": r["education"], "location": r.get("location", ""), "summary": r["summary"]}})
    index.upsert(resume_vectors)
    print(f"   ✅ {len(RESUMES)} resumes indexed.")
    print(f"\n💼 Ingesting {len(JOBS)} jobs...")
    job_texts = [build_job_text(j) for j in JOBS]
    job_embeddings = model.encode(job_texts, show_progress_bar=False)
    job_vectors = []
    for j, emb in zip(JOBS, job_embeddings):
        job_vectors.append({"id": j["id"], "vector": emb.tolist(), "meta": {"type": "job", "title": j["title"], "company": j["company"], "location": j.get("location", ""), "required_skills": j["required_skills"], "responsibilities": j["responsibilities"], "description": j["description"], "experience_required": j.get("experience_required", "")}})
    index.upsert(job_vectors)
    print(f"   ✅ {len(JOBS)} jobs indexed.")
    print(f"\n🎉 Done! {len(RESUMES)+len(JOBS)} total vectors stored in Endee!")

if __name__ == "__main__":
    ingest_all(reset="--reset" in sys.argv)

