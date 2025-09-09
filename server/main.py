from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from rq.job import Job
from .tasks import q, redis_conn
import os

app = FastAPI(title="Autonomous Data Pipeline API", version="1.0.0")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

app.mount("/outputs", StaticFiles(directory="output"), name="outputs")

UPLOADS_DIR = "uploaded_files"
os.makedirs(UPLOADS_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Autonomous Data Pipeline API!"}

@app.post("/api/v1/analyze", status_code=202)
async def analyze_data(file: UploadFile = File(...), goal: str = Form(...)):
    try:
        file_path = os.path.join(UPLOADS_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        job = q.enqueue('server.tasks.run_analysis_pipeline_task', file_path, goal)
        return {"job_id": job.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start analysis: {e}")

@app.get("/api/v1/status/{job_id}")
def get_task_status(job_id: str):
    
    job = Job.fetch(job_id, connection=redis_conn)
    
    return {
        "job_id": job.id,
        "status": job.get_status(),
        "progress": job.meta.get('progress', '0%'),
        "current_step": job.meta.get('status', 'Waiting in queue...'),
        "result": job.result
    }

@app.get("/api/v1/results/{job_id}")
def get_results(job_id: str):
    job = Job.fetch(job_id, connection=redis_conn)
    if not job.is_finished:
        raise HTTPException(status_code=404, detail="Job not complete.")
    
    output_files = job.result.get("output_files", [])
    return {
        "job_id": job.id,
        "result_urls": [f"/outputs/{file}" for file in output_files]
    }

@app.post("/api/v1/chat")
async def chat_with_data(payload: dict):
    question = payload.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="A 'question' field is required.")
    response = "This is a placeholder response. RAG chain is not yet implemented."
    return {"answer": response}