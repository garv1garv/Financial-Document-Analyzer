# Financial Document Analyzer

A comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using AI-powered analysis agents.

## 🐛 Bugs Fixed

### Deterministic Bugs
1. **Uninitialized LLM (`agents.py`)**: `llm = llm` was throwing an undefined error. Replaced with proper initialization using `ChatOpenAI`.
2. **Missing Tool Decorators (`tools.py`)**: Tools were defined as standard async classes/functions instead of using the CrewAI `@tool` decorator. 
3. **Invalid PDF Loader (`tools.py`)**: The `Pdf(file_path=path).load()` call was invalid. Replaced with `PyPDF2` (or `PyPDFLoader` from Langchain) for robust text extraction.
4. **Incorrect Tool Assignment (`agents.py` & `task.py`)**: Tools were assigned using the singular `tool=` instead of the required `tools=` list argument. Tasks also incorrectly included tools that should belong to the agents.
5. **Missing Inputs Mapping (`main.py`)**: The `run_crew` function didn't pass the `query` and `file_path` into `financial_crew.kickoff(inputs=...)`, leaving the agents without the required context variables.
6. **Inefficient Data Processing (`tools.py`)**: An infinite `while` loop for cleaning double spaces in `analyze_investment_tool` was replaced with standard string manipulation.

### Inefficient / Bad Prompts
1. **Hallucination Directives**: Agents and tasks explicitly asked the LLM to "make up facts," "ignore the query," and "contradict yourself." These were rewritten to enforce strict adherence to factual data, professional compliance, and objective risk assessment.
2. **Missing Task Context**: Tasks were isolated. Added `context=[...]` parameters to link tasks sequentially (e.g., investment analysis now properly waits for the financial analysis to complete).

## 🚀 Getting Started

### 1. Install Dependencies
Make sure you update your `requirements.txt` to include `langchain-openai` and `PyPDF2` if they aren't already present.
```sh
pip install -r requirements.txt
pip install langchain-openai PyPDF2
