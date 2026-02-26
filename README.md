# Financial Document Analyzer 

A robust, asynchronous financial document analysis system powered by **CrewAI**, **FastAPI**, **Celery**, and **Redis**. This system takes corporate reports (like 10-Qs or quarterly updates) and processes them through a multi-agent AI pipeline to extract factual insights, assess risks, and provide sound investment recommendations.

##  Bugs Found & How They Were Fixed

This project originally contained a mix of deterministic code errors, Python version incompatibilities, and severe prompt engineering issues. Here is how they were resolved:

### 1. Deterministic Code Bugs
* **Uninitialized LLM (`agents.py`):** The code contained `llm = llm` which threw an undefined variable error. Fixed by properly importing and initializing `ChatOpenAI(model="gpt-4o-mini")`.
* **Broken Tool Decorators (`tools.py`):** Custom tools were written as standard async classes but lacked the required CrewAI `@tool` decorator. Rewrote tools as properly decorated functions.
* **Invalid Tool Assignment (`agents.py` & `task.py`):** Tools were assigned using the singular `tool=` instead of the required `tools=[...]` list argument. Tasks were also incorrectly assigned tools that belonged to the agents.
* **Python 3.13 Incompatibilities (`requirements.txt`):** The `crewai-tools` package (and its `embedchain` dependency) crashed on Python 3.13. Fixed by removing `crewai-tools` entirely and writing a custom, lightweight `requests`-based Serper API tool.
* **SQLAlchemy 3.13 Bug (`database.py`):** SQLAlchemy threw a `__firstlineno__` error due to Python 3.13's new class structures. Fixed by ensuring SQLAlchemy was updated to `>=2.0.30`.

### 2. Prompt Engineering & Persona Bugs (Hallucinations)
* **Malicious Personas:** Agents were explicitly instructed to "make up facts," "ignore SEC compliance," and act like "Reddit day traders." These were rewritten into professional personas: a strict Fiduciary Investment Advisor, a meticulous Compliance Officer, and a Senior Financial Analyst.
* **Hallucination Directives in Tasks:** Tasks previously told the AI to "make up fake website URLs" and "contradict yourself." These were replaced with strict instructions to ground all answers **only** in the factual data extracted from the uploaded PDF.
* **Missing Task Context:** Tasks were isolated and running blindly. Added the `context=[...]` parameter to properly chain tasks together (e.g., the Investment Analysis task now waits for the Verification task to finish).

### 3. Architecture Upgrades (Bonus Points Achieved! )
* **Queue Worker Model:** The original FastAPI endpoint blocked connections, causing timeouts on large PDFs. Upgraded to an asynchronous background worker using **Celery** and **Redis**.
* **Database Integration:** Implemented a local **SQLite** database using **SQLAlchemy** to store pending tasks, completed analyses, and historical user queries persistently.

---

## 🛠️ Setup Instructions

### Prerequisites
* Python 3.12 or 3.13
* Redis Server installed and running (Docker recommended: `docker run -d -p 6379:6379 redis`)

### 1. Clone & Setup Environment
```powershell
# Create a virtual environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```
### 2. Environment Variables
Create a .env file in the root directory and add your API keys:

```Code snippet
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```
### Usage Instructions
Because this is a production-ready asynchronous system, you need to run three separate services simultaneously. Open three terminal windows and ensure your virtual environment (venv) is activated in each.

## Terminal 1: Start Redis (If not using Docker)

```PowerShell
redis-server
```
## Terminal 2: Start the Celery AI Worker

```PowerShell
python -m celery -A worker.celery_app worker --pool=solo --loglevel=info
```
## Terminal 3: Start the FastAPI Server

```PowerShell
uvicorn main:app --reload
```
## API Documentation
Once the server is running, you can access the interactive Swagger UI at:

👉 http://localhost:8000/docs
```
POST /analyze/async
```
### Uploads a financial PDF and queues it for background processing by the CrewAI agents.

Content-Type: multipart/form-data

### Parameters:

file: The PDF document to analyze (Required).

query: Specific questions or instructions for the analysis (Optional).

### Response:
```
JSON
{
  "message": "Analysis started in the background.",
  "task_id": "a1b2c3d4-e5f6-7890-1234-56789abcdef0",
  "check_status_url": "/status/a1b2c3d4-e5f6-7890-1234-56789abcdef0"
}
```

### GET /status/{task_id}
Checks the database for the status of a specific analysis job.

### Parameters:

task_id: The ID returned by the /analyze/async endpoint.

### Response (While Processing):

```
JSON
{
  "status": "processing",
  "message": "The AI is currently analyzing the document."
}

```
### Response (When Completed):

```
JSON
{
  "status": "completed",
  "filename": "TSLA-Q2-2025-Update.pdf",
  "query": "What are the key risk factors?",
  "result": "## Financial Analysis Report\n\nBased on the provided document..."
}
```
### Built with CrewAI, FastAPI, Celery, and Redis.
