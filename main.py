from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
from worker import process_financial_document_task
from database import SessionLocal, AnalysisRecord

app = FastAPI(title="Financial Document Analyzer")

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze/async")
async def analyze_document_async(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """Uploads a document and queues it for background analysis."""
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    os.makedirs("data", exist_ok=True)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
        
    task = process_financial_document_task.delay(
        query=query.strip(), 
        file_path=file_path, 
        filename=file.filename
    )
    
    return {
        "message": "Analysis started in the background.",
        "task_id": task.id,
        "check_status_url": f"/status/{task.id}"
    }

@app.get("/status/{task_id}")
async def get_task_status(task_id: str):
    """Check the database for the status of a specific task."""
    db = SessionLocal()
    try:
        record = db.query(AnalysisRecord).filter(AnalysisRecord.id == task_id).first()
        if not record:
            raise HTTPException(status_code=404, detail="Task not found")
            
        if record.status == "completed":
            return {
                "status": record.status, 
                "filename": record.filename,
                "query": record.query,
                "result": record.result_text
            }
        else:
            return {
                "status": record.status, 
                "message": "The AI is currently analyzing the document."
            }
    finally:
        db.close()