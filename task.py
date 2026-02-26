from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor

verification = Task(
    description="Read the document at {file_path}. Verify if it is a valid financial report.",
    expected_output="Confirmation of whether the document is a financial report.",
    agent=verifier,
    async_execution=False
)

analyze_financial_document = Task(
    description="Based on the verified document at {file_path}, analyze the financials to address: '{query}'.",
    expected_output="A detailed financial analysis report addressing the user's query with factual data.",
    agent=financial_analyst,
    context=[verification],
    async_execution=False,
)

investment_analysis = Task(
    description="Using the financial analysis, provide professional, evidence-based investment advice.",
    expected_output="A bulleted list of investment recommendations grounded in the financial analysis.",
    agent=investment_advisor,
    context=[analyze_financial_document],
    async_execution=False,
)

risk_assessment = Task(
    description="Evaluate the risk factors present in the financial document.",
    expected_output="A structured risk assessment report detailing potential risks and mitigation strategies.",
    agent=risk_assessor,
    context=[analyze_financial_document],
    async_execution=False,
)