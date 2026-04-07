"""API routes for the AI Agent RAG System."""

from fastapi import APIRouter, HTTPException, status
from datetime import datetime
import time
import logging

from app.models import (
    AskRequest,
    AskResponse,
    HealthResponse,
    SessionHistoryResponse,
    ConversationMessage,
    ErrorResponse,
    DecisionType
)
from app.agent.core import agent
from app.agent.memory import session_manager
from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/ask",
    response_model=AskResponse,
    status_code=status.HTTP_200_OK,
    summary="Ask the AI agent a question",
    description="Submit a query to the AI agent. The agent will decide whether to answer directly or search documents.",
    responses={
        200: {"description": "Successful response"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    }
)
async def ask_question(request: AskRequest) -> AskResponse:
    """
    Process a user query and return an answer.

    The agent will:
    1. Determine if the query needs document search or can be answered directly
    2. Use appropriate tools (document_search, calculator) if needed
    3. Maintain conversation context using the session_id
    4. Return a structured response with sources (if applicable)
    """
    logger.info(f"Received ask request: query='{request.query[:50]}...', session={request.session_id}")

    start_time = time.time()

    try:
        # Process the query using the agent
        result = await agent.process_query(
            query=request.query,
            session_id=request.session_id
        )

        # Calculate processing time
        processing_time_ms = (time.time() - start_time) * 1000

        # Build response
        response = AskResponse(
            answer=result["answer"],
            sources=result.get("sources", []),
            decision=DecisionType(result["decision"]),
            session_id=result["session_id"],
            confidence=result.get("confidence"),
            processing_time_ms=round(processing_time_ms, 2)
        )

        logger.info(
            f"Request processed successfully: session={response.session_id}, "
            f"decision={response.decision}, time={processing_time_ms:.2f}ms"
        )

        return response

    except Exception as e:
        logger.error(f"Error processing ask request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process query: {str(e)}"
        )


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check endpoint",
    description="Check the health status of the application and its dependencies.",
)
async def health_check() -> HealthResponse:
    """
    Check application health and service connectivity.

    Returns:
        Health status including Groq and vector store connectivity
    """
    logger.debug("Health check requested")

    try:
        # TODO: Add actual connectivity checks for Groq and vector store
        # For now, return basic health status

        return HealthResponse(
            status="healthy",
            timestamp=datetime.utcnow(),
            llm_provider="connected",  # TODO: Implement actual check
            vector_store="pending",   # TODO: Implement actual check (needs indexed data)
            version=settings.APP_VERSION
        )

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=True)
        return HealthResponse(
            status="unhealthy",
            timestamp=datetime.utcnow(),
            llm_provider="unknown",
            vector_store="unknown",
            version=settings.APP_VERSION
        )


@router.get(
    "/sessions/{session_id}/history",
    response_model=SessionHistoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get conversation history for a session",
    description="Retrieve the conversation history for a specific session ID.",
)
async def get_session_history(session_id: str) -> SessionHistoryResponse:
    """
    Retrieve conversation history for a session.

    Args:
        session_id: The session ID to retrieve history for

    Returns:
        Conversation history with messages
    """
    logger.info(f"Retrieving history for session: {session_id}")

    try:
        session = session_manager.get_or_create_session(session_id)
        history = session.get_conversation_history()

        messages = [
            ConversationMessage(
                role=msg["role"],
                content=msg["content"],
                timestamp=datetime.utcnow()  # TODO: Use actual message timestamp
            )
            for msg in history
        ]

        return SessionHistoryResponse(
            session_id=session_id,
            messages=messages,
            message_count=len(messages)
        )

    except Exception as e:
        logger.error(f"Error retrieving session history: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve session history: {str(e)}"
        )


@router.delete(
    "/sessions/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a session",
    description="Clear the conversation history and delete a session.",
)
async def delete_session(session_id: str):
    """
    Delete a session and clear its conversation history.

    Args:
        session_id: The session ID to delete

    Returns:
        204 No Content on success
    """
    logger.info(f"Deleting session: {session_id}")

    try:
        deleted = session_manager.delete_session(session_id)

        if not deleted:
            logger.warning(f"Session not found: {session_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session {session_id} not found"
            )

        logger.info(f"Session deleted successfully: {session_id}")
        return None

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete session: {str(e)}"
        )


@router.get(
    "/sessions/stats",
    status_code=status.HTTP_200_OK,
    summary="Get session statistics",
    description="Get statistics about active sessions.",
)
async def get_session_stats():
    """
    Get statistics about active sessions.

    Returns:
        Dict with session statistics
    """
    logger.debug("Session stats requested")

    try:
        # Cleanup expired sessions first
        cleaned_up = session_manager.cleanup_expired_sessions()

        return {
            "active_sessions": session_manager.get_active_session_count(),
            "expired_sessions_cleaned": cleaned_up,
            "max_messages_per_session": settings.AGENT_MEMORY_MAX_MESSAGES,
            "session_ttl_minutes": settings.AGENT_SESSION_TTL_MINUTES
        }

    except Exception as e:
        logger.error(f"Error getting session stats: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get session stats: {str(e)}"
        )
