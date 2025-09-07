import redis
from rq import Queue, get_current_job
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipeline import run_pipeline as run_main_pipeline


redis_conn = redis.from_url("redis://localhost:6379")

q = Queue(connection=redis_conn)

def run_analysis_pipeline_task(file_path: str, goal: str):
    
    job = get_current_job()
    print(f"RQ worker: Starting job {job.id} for file: {file_path}")
    
    result = run_main_pipeline(job, file_path, goal)
    
    print(f"RQ worker: Finished job {job.id} for file: {file_path}")
    return result