import os
from celery import Celery
from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import analyze_financial_document, verification, investment_analysis, risk_assessment
from database import SessionLocal, AnalysisRecord

celery_app = Celery(
    "financial_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

def run_crew(query: str, file_path: str):
    """Executes the CrewAI process."""
    financial_crew = Crew(
        agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
        tasks=[verification, analyze_financial_document, investment_analysis, risk_assessment],
        process=Process.sequential,
        verbose=True
    )
    return financial_crew.kickoff(inputs={'query': query, 'file_path': file_path})

@celery_app.task(bind=True)
def process_financial_document_task(self, query: str, file_path: str, filename: str):
    db = SessionLocal()

    record = AnalysisRecord(id=self.request.id, filename=filename, query=query, status="processing")
    db.add(record)
    db.commit()

    try:
        result = run_crew(query=query, file_path=file_path)
        record.status = "completed"
        record.result_text = str(getattr(result, 'raw', str(result)))
        db.commit()
        
    except Exception as e:
        record.status = "failed"
        record.result_text = str(e)
        db.commit()
        
    finally:
        db.close()
        if os.path.exists(file_path):
            os.remove(file_path)
            
    return record.status