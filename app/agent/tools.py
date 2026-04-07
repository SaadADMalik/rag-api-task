"""Agent tools for document search and calculations."""

from typing import Dict, Any, List
import re
import logging
from langchain.tools import Tool
from langchain.pydantic_v1 import BaseModel, Field

logger = logging.getLogger(__name__)


# ============================================================================
# Tool Input Schemas
# ============================================================================

class DocumentSearchInput(BaseModel):
    """Input schema for document search tool."""
    query: str = Field(..., description="Search query to find relevant documents")


class CalculatorInput(BaseModel):
    """Input schema for calculator tool."""
    expression: str = Field(
        ...,
        description="Mathematical expression to evaluate (e.g., '2 + 2', '15 * 3.5')"
    )


# ============================================================================
# Tool Functions
# ============================================================================

def document_search(query: str) -> str:
    """
    Search company policy documents for relevant information.

    Args:
        query: Search query string

    Returns:
        Formatted string with relevant document chunks and sources
    """
    logger.info(f"Document search called with query: {query}")

    try:
        # Import retriever (lazy import to avoid circular dependencies)
        from app.rag.retriever import retriever

        # Retrieve relevant documents
        documents = retriever.retrieve(query)

        if not documents:
            return (
                "I couldn't find any relevant information in the company policy documents "
                "for your query. You may want to contact HR directly for assistance."
            )

        # Format context for LLM
        context = retriever.format_context(documents)

        # Add source summary
        sources = retriever.get_sources_summary(documents)
        source_names = [s['document'] for s in sources]

        result = f"**Relevant Information Found:**\n\n{context}\n\n"
        result += f"**Sources:** {', '.join(source_names)}"

        logger.info(f"Document search returned {len(documents)} results from {len(sources)} sources")

        return result

    except Exception as e:
        logger.error(f"Error in document search: {str(e)}", exc_info=True)
        return (
            f"I encountered an error while searching the documents: {str(e)}. "
            "Please try rephrasing your question or contact IT support."
        )


def safe_calculate(expression: str) -> str:
    """
    Safely evaluate a mathematical expression.

    Supports basic arithmetic operations: +, -, *, /, **, %, ()

    Args:
        expression: Mathematical expression as string

    Returns:
        Result as string, or error message if evaluation fails

    Example:
        >>> safe_calculate("2 + 2")
        "4"
        >>> safe_calculate("(10 + 5) * 3")
        "45"
    """
    logger.info(f"Calculator called with expression: {expression}")

    try:
        # Remove any whitespace
        expression = expression.strip()

        # Security: Only allow numbers, operators, parentheses, and decimal points
        if not re.match(r'^[\d\+\-\*\/\(\)\.\s\%\*\*]+$', expression):
            return (
                f"Error: Invalid expression '{expression}'. "
                "Only numbers and operators (+, -, *, /, **, %, parentheses) are allowed."
            )

        # Security: Prevent expressions that are too long (potential DoS)
        if len(expression) > 200:
            return "Error: Expression is too long. Maximum 200 characters allowed."

        # Evaluate the expression
        result = eval(expression, {"__builtins__": {}}, {})

        # Format the result nicely
        if isinstance(result, float):
            # Round to 6 decimal places to avoid floating point artifacts
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 6)

        logger.info(f"Calculation result: {expression} = {result}")
        return str(result)

    except ZeroDivisionError:
        error_msg = "Error: Division by zero"
        logger.warning(f"Calculator error: {error_msg}")
        return error_msg

    except SyntaxError:
        error_msg = f"Error: Invalid syntax in expression '{expression}'"
        logger.warning(f"Calculator error: {error_msg}")
        return error_msg

    except Exception as e:
        error_msg = f"Error: Failed to evaluate expression. {str(e)}"
        logger.error(f"Calculator error: {error_msg}")
        return error_msg


# ============================================================================
# LangChain Tool Definitions
# ============================================================================

def create_tools() -> List[Tool]:
    """
    Create and return all available agent tools.

    Returns:
        List of LangChain Tool objects
    """
    tools = []

    # Document Search Tool
    document_search_tool = Tool(
        name="document_search",
        func=document_search,
        description=(
            "Search company policy documents to find relevant information. "
            "Use this when the user asks about company policies, procedures, "
            "benefits, leave policies, security guidelines, expense policies, "
            "or any other company-related information. "
            "Input should be a clear search query describing what you're looking for."
        ),
        args_schema=DocumentSearchInput,
    )
    tools.append(document_search_tool)

    # Calculator Tool
    calculator_tool = Tool(
        name="calculator",
        func=safe_calculate,
        description=(
            "Evaluate mathematical expressions. "
            "Supports basic arithmetic: addition (+), subtraction (-), "
            "multiplication (*), division (/), exponentiation (**), modulo (%), "
            "and parentheses for grouping. "
            "Input should be a valid mathematical expression like '2 + 2' or '(10 * 5) / 2'."
        ),
        args_schema=CalculatorInput,
    )
    tools.append(calculator_tool)

    logger.info(f"Created {len(tools)} agent tools: {[t.name for t in tools]}")
    return tools


# ============================================================================
# Tool Connection Point for RAG
# ============================================================================

class ToolConnector:
    """
    Connector to plug in the RAG retriever to the document_search tool.

    This will be used once the RAG pipeline is implemented.
    """

    _retriever = None

    @classmethod
    def set_retriever(cls, retriever):
        """
        Set the RAG retriever to be used by document_search tool.

        Args:
            retriever: RAG retriever instance
        """
        cls._retriever = retriever
        logger.info("RAG retriever connected to document_search tool")

    @classmethod
    def get_retriever(cls):
        """Get the current retriever instance."""
        return cls._retriever

    @classmethod
    def search_documents(cls, query: str) -> str:
        """
        Search documents using the connected retriever.

        Args:
            query: Search query

        Returns:
            Formatted search results
        """
        if cls._retriever is None:
            return (
                "RAG retriever not yet initialized. "
                "Please wait for document indexing to complete."
            )

        try:
            # This will be implemented when we connect the RAG pipeline
            results = cls._retriever.retrieve(query)
            return results
        except Exception as e:
            logger.error(f"Error in document search: {str(e)}")
            return f"Error searching documents: {str(e)}"
