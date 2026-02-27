## Importing libraries and files
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from crewai_tools import tools
from crewai_tools import SerperDevTool

try:
    from PyPDF2 import PdfReader
except Exception:
    PdfReader = None

## Creating search tool (stub)
search_tool = SerperDevTool()


class FinancialDocumentTool:
    @staticmethod
    async def read_data_tool(path: str = 'data/sample.pdf') -> str:
        """Read text content from a PDF file at `path`.

        Falls back to returning raw bytes->utf-8 decoded text if PDF parsing is unavailable.
        """
        if not os.path.exists(path):
            return ""

        if PdfReader is not None:
            try:
                reader = PdfReader(path)
                full_report = []
                for page in reader.pages:
                    text = page.extract_text() or ""
                    # Normalize whitespace
                    text = '\n'.join([line.strip() for line in text.splitlines() if line.strip()])
                    full_report.append(text)
                return "\n\n".join(full_report)
            except Exception:
                pass

        # Fallback: try to read as text
        try:
            with open(path, 'rb') as f:
                data = f.read()
            try:
                return data.decode('utf-8', errors='ignore')
            except Exception:
                return ''
        except Exception:
            return ''


class InvestmentTool:
    @staticmethod
    async def analyze_investment_tool(financial_document_data: str) -> str:
        # Basic safe placeholder analysis: summary statistics of the text
        if not financial_document_data:
            return "No document content available for investment analysis."

        words = financial_document_data.split()
        num_words = len(words)
        num_chars = len(financial_document_data)
        return f"Document size: {num_words} words, {num_chars} characters. Detailed analysis not implemented."


class RiskTool:
    @staticmethod
    async def create_risk_assessment_tool(financial_document_data: str) -> str:
        if not financial_document_data:
            return "No document content available for risk assessment."
        # Minimal safe risk assessment placeholder
        return "Basic risk check complete. Detailed risk models are not implemented in this debug build."
