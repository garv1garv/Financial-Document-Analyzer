import os
from dotenv import load_dotenv
from crewai import Agent
from langchain_openai import ChatOpenAI
from tools import search_tool, read_data_tool, analyze_investment_tool, create_risk_assessment_tool

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Analyze financial documents to extract accurate insights and answer the user query: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are an experienced financial analyst known for rigorous analysis and "
        "objective market assessments. You rely strictly on factual data."
    ),
    tools=[read_data_tool, search_tool],
    llm=llm,
    max_iter=2,
    allow_delegation=True
)

verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify the authenticity and relevance of the provided document at {file_path}.",
    verbose=True,
    memory=True,
    backstory="You are a strict compliance officer ensuring documents are factual corporate reports.",
    tools=[read_data_tool],
    llm=llm,
    max_iter=1,
    allow_delegation=False
)

investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide sound, evidence-based investment recommendations.",
    verbose=True,
    backstory="A fiduciary investment advisor prioritizing regulatory compliance and risk management.",
    tools=[analyze_investment_tool],
    llm=llm,
    max_iter=1,
    allow_delegation=False
)

risk_assessor = Agent(
    role="Risk Assessment Expert",
    goal="Identify and quantify potential risks mentioned in the financial document.",
    verbose=True,
    backstory="A meticulous risk manager who identifies operational, market, and liquidity risks.",
    tools=[create_risk_assessment_tool],
    llm=llm,
    max_iter=1,
    allow_delegation=False
)