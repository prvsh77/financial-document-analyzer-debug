## Importing libraries and files
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from crewai import Agent
from tools import search_tool, FinancialDocumentTool

# Minimal LLM placeholder (replace with a real client when available)
llm = None

# Create a simple, safe financial analyst agent
financial_analyst = Agent(
    role="Financial Analyst",
    goal="Provide a careful, evidence-based summary of the uploaded financial document: {query}",
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
)

# Verifier agent - lightweight, performs basic checks
verifier = Agent(
    role="Document Verifier",
    goal="Check whether the uploaded file appears to be a PDF and contains readable text.",
    tools=[],
    llm=llm,
)

# Additional example agents (safe placeholders)
investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide high-level investment considerations based on the document.",
    tools=[],
    llm=llm,
)

risk_assessor = Agent(
    role="Risk Assessor",
    goal="Provide a basic risk summary based on observable document content.",
    tools=[],
    llm=llm,
)
