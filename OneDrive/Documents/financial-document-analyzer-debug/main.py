import os
import uuid
import asyncio

try:
    from fastapi import FastAPI, File, UploadFile, Form, HTTPException
    FASTAPI_AVAILABLE = True
except Exception:
    FASTAPI_AVAILABLE = False

from crewai import Crew, Process
from agents import financial_analyst
from task import analyze_financial_document as analyze_task

# database and queue imports
from db import SessionLocal, Analysis, init_db

# Try to import Redis and RQ, but make them optional
REDIS_AVAILABLE = False
try:
    from redis import Redis
    from rq import Queue
    redis_conn = Redis()
    queue = Queue('financial', connection=redis_conn)
    REDIS_AVAILABLE = True
except Exception as e:
    print(f"Warning: Redis/RQ not available: {e}")
    print("Running in synchronous mode without background tasks")
    redis_conn = None
    queue = None


if FASTAPI_AVAILABLE:
    app = FastAPI(title="Financial Document Analyzer")

# ensure database tables exist
init_db()
def run_crew(query: str, file_path: str="data/sample.pdf"):
    """To run the whole crew"""
    financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[analyze_task],
        process=Process.sequential,
    )
    
    # Pass both query and file_path into the task context
    result = financial_crew.kickoff({'query': query, 'file_path': file_path})
    return result

if FASTAPI_AVAILABLE:
    @app.get("/")
    async def root():
        """Health check endpoint"""
        return {"message": "Financial Document Analyzer API is running"}

    @app.get("/status/{job_id}")
    async def job_status(job_id: str):
        """Return status and result of a queued analysis"""
        session = SessionLocal()
        record = session.get(Analysis, job_id)
        session.close()
        if not record:
            raise HTTPException(status_code=404, detail="Job not found")
        return {"job_id": record.id, "status": record.status, "result": record.result}

    @app.post("/analyze")
    async def analyze_financial_document(
        file: UploadFile = File(...),
        query: str = Form(default="Analyze this financial document for investment insights")
    ):
        """Analyze financial document and provide comprehensive investment recommendations"""
        
        file_id = str(uuid.uuid4())
        file_path = f"data/financial_document_{file_id}.pdf"
        
        try:
            # Ensure data directory exists
            os.makedirs("data", exist_ok=True)
            
            # Save uploaded file
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            
            # Validate query
            if query=="" or query is None:
                query = "Analyze this financial document for investment insights"
                
            # record job in database
            session = SessionLocal()
            job = Analysis(query=query.strip(), file_path=file_path, status="pending")
            session.add(job)
            session.commit()
            session.refresh(job)
            job_id = job.id
            session.close()

            # Choose between background processing (Redis) or synchronous processing
            if REDIS_AVAILABLE:
                # enqueue the processing task
                from worker import process_job
                queue.enqueue(process_job, job_id, query.strip(), file_path)
                return {
                    "status": "queued",
                    "job_id": job_id,
                    "query": query,
                    "file_processed": file.filename
                }
            else:
                # Process synchronously without Redis
                try:
                    result = run_crew(query=query.strip(), file_path=file_path)
                    session = SessionLocal()
                    job = session.get(Analysis, job_id)
                    job.result = str(result)
                    job.status = 'completed'
                    session.commit()
                    session.close()
                    return {
                        "status": "completed",
                        "job_id": job_id,
                        "query": query,
                        "file_processed": file.filename,
                        "result": str(result)
                    }
                except Exception as e:
                    session = SessionLocal()
                    job = session.get(Analysis, job_id)
                    job.result = f"error: {e}"
                    job.status = 'failed'
                    session.commit()
                    session.close()
                    raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error queuing financial document: {str(e)}")
        
        # note: do not remove file here; worker may need it later or implement cleanup separately


if __name__ == "__main__":
    if not FASTAPI_AVAILABLE:
        print("FastAPI is not installed. Install dependencies to run the HTTP server.")
    else:
        try:
            import uvicorn
            uvicorn.run(app, host="0.0.0.0", port=8000)
        except Exception:
            print("uvicorn is not available; run 'python main.py' with uvicorn installed or use 'uvicorn main:app'.")