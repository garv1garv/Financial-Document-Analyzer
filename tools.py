import os
import re
import requests
import json
from dotenv import load_dotenv
from crewai.tools import tool

load_dotenv()

@tool("Search the Internet")
def search_tool(query: str) -> str:
    """Useful to search the internet about a given topic and return relevant results."""
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': os.getenv("SERPER_API_KEY", ""),
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        response_data = response.json()
        
        results = []
        if 'organic' in response_data:
            for item in response_data['organic'][:4]:
                results.append(f"Title: {item.get('title')}\nSnippet: {item.get('snippet')}\n")
        
        return "\n".join(results) if results else "No useful search results found."
    except Exception as e:
        return f"Search failed: {str(e)}"

@tool("Read Financial Document")
def read_data_tool(path: str) -> str:
    """Tool to read data from a pdf file from a given path."""
    try:
        import PyPDF2
        full_report = ""
        with open(path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                content = page.extract_text()
                if content:
                    full_report += content + "\n"
        
        full_report = re.sub(r'\n+', '\n', full_report)
        return full_report
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

@tool("Investment Analysis Data Processor")
def analyze_investment_tool(financial_document_data: str) -> str:
    """Process and clean financial document data for investment analysis."""
    processed_data = " ".join(financial_document_data.split())
    return processed_data[:5000]

@tool("Risk Assessment Simulator")
def create_risk_assessment_tool(financial_document_data: str) -> str:
    """Simulates risk assessment extraction from financial data."""
    return "Standard risk assessment complete. Please review qualitative metrics carefully."