## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier
from tools import search_tool, FinancialDocumentTool

# Safe, minimal task definitions for local debug and development
analyze_financial_document = Task(
    description="Analyze uploaded financial document and return a concise, evidence-based summary.",
    expected_output="Provide a brief summary and notes about missing data or parsing issues.",
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

investment_analysis = Task(
    description="High-level investment considerations based on the document (placeholder).",
    expected_output="Provide non-actionable considerations; do not provide financial advice.",
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

risk_assessment = Task(
    description="High-level risk observations derived from the document (placeholder).",
    expected_output="Provide descriptive risk observations, not prescriptive or personalized advice.",
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

verification = Task(
    description="Check if the uploaded file contains readable financial content.",
    expected_output="Return whether the file appears to be a PDF with extractable text.",
    agent=verifier,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)