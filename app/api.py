import re
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
import uuid
import os
import threading
import queue
import json

from main import scrape_novel 

app = FastAPI()

HISTORY_FILE = "jobs_history.json"
job_queue = queue.Queue()

# Load history from file on startup
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_history(history_data):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history_data, f)

jobs = load_history()

class ScrapeRequest(BaseModel):
    start_url: str
    novel_name: str
    author: str = ""       # New!
    wait: bool = True
    cover_data: str = ""   # Changed from cover_url

def background_worker():
    while True:
        job_data = job_queue.get() 
        job_id = job_data["job_id"]
        
        jobs[job_id]["status"] = "processing"
        save_history(jobs)
        
        try:
            print(f"Starting job from queue: {job_id}")
            scrape_novel(job_data)
            jobs[job_id]["status"] = "completed"
        except Exception as e:
            jobs[job_id]["status"] = f"failed: {str(e)}"
        finally:
            save_history(jobs)
            job_queue.task_done()

@app.on_event("startup")
def startup_event():
    threading.Thread(target=background_worker, daemon=True).start()

@app.get("/", response_class=HTMLResponse)
def serve_ui():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/start-scrape")
def start_scrape(req: ScrapeRequest):
    job_id = str(uuid.uuid4())
    
    jobs[job_id] = {
        "novel_name": req.novel_name,
        "status": "queued"
    }
    save_history(jobs)
    
    job_data = {
        "job_id": job_id,
        "start_url": req.start_url,
        "novel_name": req.novel_name,
        "author": req.author,          # Pass it to the scraper
        "wait": req.wait,
        "cover_data": req.cover_data   # Pass it to the scraper
    }
    job_queue.put(job_data)
    
    return {"job_id": job_id, "status": "Added to queue"}

@app.get("/api/status/{job_id}")
def check_status(job_id: str):
    job_info = jobs.get(job_id, {"status": "not found"})
    status = job_info.get("status", "not found")
    progress_text = "0 chapters scraped"
    
    progress_file = f"{job_id}_progress.jsonl"
    if os.path.exists(progress_file):
        try:
            with open(progress_file, "r", encoding="utf-8") as f:
                chapter_count = sum(1 for _ in f)
            progress_text = f"{chapter_count} chapters scraped..."
        except Exception:
            pass
            
    return {"job_id": job_id, "status": status, "progress": progress_text}

# NEW: Send the whole library to the UI
@app.get("/api/history")
def get_history():
    return jobs

@app.get("/api/download/{job_id}")
def download_epub(job_id: str):
    file_path = f"{job_id}.epub"
    
    if os.path.exists(file_path):
        # 1. Look up the real novel name from our history database
        job_info = jobs.get(job_id, {})
        raw_name = job_info.get("novel_name", "Scraped_Novel")
        
        # 2. Sanitize the name so it doesn't break Windows/Mac file systems
        # This removes illegal characters like \ / : * ? " < > |
        safe_name = re.sub(r'[\\/*?:"<>|]', "", raw_name)
        
        # Replace spaces with underscores for a cleaner downloaded file
        safe_name = safe_name.replace(" ", "_")
        
        # 3. Send the file using the beautiful, clean name!
        download_name = f"{safe_name}.epub"
        
        return FileResponse(file_path, media_type='application/epub+zip', filename=download_name)
        
    return {"error": "File not ready or does not exist"}