"""Pydantic models for API requests and responses."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class DecisionType(str, Enum):
    """Agent decision types."""
    DIRECT_ANSWER = "direct_answer"
    RAG_SEARCH = "rag_search"
    TOOL_USE = "tool_use"


class SourceDocument(BaseModel):
    """Source document reference."""
    document: str = Field(..., description="Document filename")
    page: Optional[int] = Field(None, description="Page number in document")
    relevance_score: float = Field(..., description="Relevance score (0-1)")
    snippet: Optional[str] = Field(None, description="Relevant text snippet")


class AskRequest(BaseModel):
    """Request model for /ask endpoint."""
    query: str = Field(..., min_length=1, max_length=1000, description="User query")
    session_id: Optional[str] = Field(
        None,
        description="Optional session ID for conversation continuity"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is the parental leave policy?",
                "session_id": "user-123-session-abc"
            }
        }


class AskResponse(BaseModel):
    """Response model for /ask endpoint."""
    answer: str = Field(..., description="Agent's answer to the query")
    sources: List[SourceDocument] = Field(
        default_factory=list,
        description="Source documents used (if any)"
    )
    decision: DecisionType = Field(..., description="How the agent decided to answer")
    session_id: str = Field(..., description="Session ID for this conversation")
    confidence: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Confidence score for the answer"
    )
    processing_time_ms: Optional[float] = Field(
        None,
        description="Processing time in milliseconds"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "According to our HR Handbook, parental leave policy provides 12 weeks of paid leave...",
                "sources": [
                    {
                        "document": "hr_handbook.pdf",
                        "page": 15,
                        "relevance_score": 0.89,
                        "snippet": "Parental leave: 12 weeks paid..."
                    }
                ],
                "decision": "rag_search",
                "session_id": "user-123-session-abc",
                "confidence": 0.92,
                "processing_time_ms": 1250.5
            }
        }


class HealthResponse(BaseModel):
    """Response model for /health endpoint."""
    status: str = Field(..., description="Overall health status")
    timestamp: datetime = Field(..., description="Current server timestamp")
    llm_provider: str = Field(..., description="LLM provider connection status")
    vector_store: str = Field(..., description="Vector store connection status")
    version: str = Field(..., description="Application version")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2026-04-06T12:00:00Z",
                "llm_provider": "connected",
                "vector_store": "connected",
                "version": "1.0.0"
            }
        }


class ConversationMessage(BaseModel):
    """Single message in a conversation."""
    role: str = Field(..., description="Message role (user/assistant)")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(..., description="Message timestamp")


class SessionHistoryResponse(BaseModel):
    """Response model for session history endpoint."""
    session_id: str = Field(..., description="Session ID")
    messages: List[ConversationMessage] = Field(
        default_factory=list,
        description="Conversation history"
    )
    message_count: int = Field(..., description="Total number of messages")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Query cannot be empty",
                "detail": {"field": "query"},
                "timestamp": "2026-04-06T12:00:00Z"
            }
        }
