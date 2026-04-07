import logging
import re
from typing import Any, Dict, List, Optional

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from app.config import settings
from app.agent.router import decision_router
from app.agent.memory import session_manager
from app.rag.retriever import retriever

logger = logging.getLogger(__name__)


class AIAgent:
    """
    AI Agent that can answer queries using direct knowledge or RAG.

    Capabilities:
    - Smart routing (direct answer vs document search)
    - Tool calling (document_search, calculator)
    - Session-based conversation memory
    - Context-aware responses
    """

    def __init__(self):
        """Initialize the AI agent."""
        self.llm = self._initialize_llm()
        logger.info("AIAgent initialized successfully")

    def _initialize_llm(self) -> ChatGroq:
        """Initialize Groq LLM."""
        logger.info("Initializing Groq LLM...")

        llm = ChatGroq(
            model=settings.GROQ_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=settings.GROQ_TEMPERATURE,
            max_tokens=settings.GROQ_MAX_TOKENS,
        )

        logger.info(
            f"Groq initialized: model={settings.GROQ_MODEL}, "
            f"temp={settings.GROQ_TEMPERATURE}"
        )
        return llm

    async def process_query(
        self,
        query: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a user query and return a response.

        Args:
            query: User query string
            session_id: Optional session ID for conversation continuity

        Returns:
            Dict containing answer, sources, decision type, etc.
        """
        logger.info(f"Processing query: '{query}' (session: {session_id})")

        # Get or create session
        session = session_manager.get_or_create_session(session_id)
        actual_session_id = session.session_id

        # Add user message to session
        session_manager.add_user_message(actual_session_id, query)

        # Decide whether to use RAG or direct answer
        decision, confidence = decision_router.decide(query)

        logger.info(f"Decision: {decision} (confidence: {confidence:.2f})")

        try:
            history = session_manager.get_session_history(actual_session_id)
            chat_history = self._format_chat_history(history)[:-1]

            sources: List[Dict[str, Any]] = []

            if decision == "rag_search":
                documents = retriever.retrieve(query)
                context = retriever.format_context(documents)
                sources = retriever.get_sources_summary(documents)

                messages = [
                    SystemMessage(
                        content=(
                            "You are a corporate policy assistant. Answer only using the provided context. "
                            "If context is insufficient, say you could not find enough policy detail and suggest contacting HR or IT. "
                            "When using context, include document names in the response."
                        )
                    ),
                    *chat_history,
                    HumanMessage(
                        content=(
                            f"User question: {query}\n\n"
                            f"Retrieved context:\n{context}"
                        )
                    ),
                ]
            else:
                calc = self._maybe_calculate(query)
                if calc is not None:
                    answer = calc
                    session_manager.add_assistant_message(actual_session_id, answer)
                    return {
                        "answer": answer,
                        "sources": [],
                        "decision": decision,
                        "session_id": actual_session_id,
                        "confidence": confidence if settings.ENABLE_CONFIDENCE_SCORING else None,
                    }

                messages = [
                    SystemMessage(
                        content=(
                            "You are a professional internal assistant. "
                            "Be concise, helpful, and factual."
                        )
                    ),
                    *chat_history,
                    HumanMessage(content=query),
                ]

            llm_response = await self.llm.ainvoke(messages)
            answer = getattr(llm_response, "content", str(llm_response))

            # Add assistant response to session
            session_manager.add_assistant_message(actual_session_id, answer)

            # Prepare response
            result = {
                "answer": answer,
                "sources": sources,
                "decision": decision,
                "session_id": actual_session_id,
                "confidence": confidence if settings.ENABLE_CONFIDENCE_SCORING else None,
            }

            logger.info(f"Query processed successfully for session {actual_session_id}")
            return result

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}", exc_info=True)
            return {
                "answer": f"I apologize, but I encountered an error: {str(e)}",
                "sources": [],
                "decision": "direct_answer",
                "session_id": actual_session_id,
                "confidence": 0.0,
            }

    def _format_chat_history(
        self,
        history: List[Dict[str, str]]
    ) -> List[Any]:
        """
        Format conversation history for LangChain.

        Args:
            history: List of message dicts with 'role' and 'content'

        Returns:
            List of LangChain message objects
        """
        formatted = []
        for msg in history:
            if msg["role"] == "user":
                formatted.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                formatted.append(AIMessage(content=msg["content"]))
        return formatted

    def _maybe_calculate(self, query: str) -> Optional[str]:
        """Return calculator result for simple math expressions, otherwise None."""
        normalized = query.strip().lower()
        if not re.match(r"^[\d\s\+\-\*\/\(\)\.\%]+$", normalized):
            return None

        try:
            result = eval(normalized, {"__builtins__": {}}, {})
        except Exception:
            return None

        return str(result)


# Global agent instance
agent = AIAgent()
