"""Session memory management for conversation context."""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import threading
import logging
import uuid

logger = logging.getLogger(__name__)


@dataclass
class Message:
    """Conversation message."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime


class Session:
    """Session with conversation history."""

    def __init__(self, session_id: str, max_messages: int = 10, ttl_minutes: int = 30):
        self.session_id = session_id
        self.messages: List[Message] = []
        self.max_messages = max_messages
        self.ttl_minutes = ttl_minutes
        self.created_at = datetime.utcnow()
        self.last_accessed = datetime.utcnow()

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the session."""
        self.messages.append(Message(
            role=role,
            content=content,
            timestamp=datetime.utcnow()
        ))
        self.last_accessed = datetime.utcnow()

        # Keep only the last max_messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get formatted conversation history for LLM."""
        return [
            {"role": msg.role, "content": msg.content}
            for msg in self.messages
        ]

    def is_expired(self) -> bool:
        """Check if session has expired."""
        expiry_time = self.last_accessed + timedelta(minutes=self.ttl_minutes)
        return datetime.utcnow() > expiry_time

    def get_message_count(self) -> int:
        """Get total number of messages in session."""
        return len(self.messages)


class SessionMemoryManager:
    """Manages multiple user sessions with TTL-based cleanup."""

    def __init__(self, max_messages_per_session: int = 10, session_ttl_minutes: int = 30):
        self.sessions: Dict[str, Session] = {}
        self.max_messages = max_messages_per_session
        self.ttl_minutes = session_ttl_minutes
        self._lock = threading.Lock()
        logger.info(
            f"SessionMemoryManager initialized: "
            f"max_messages={max_messages_per_session}, ttl={session_ttl_minutes}min"
        )

    def get_or_create_session(self, session_id: Optional[str] = None) -> Session:
        """Get existing session or create new one."""
        if session_id is None:
            session_id = self._generate_session_id()

        with self._lock:
            if session_id not in self.sessions:
                self.sessions[session_id] = Session(
                    session_id=session_id,
                    max_messages=self.max_messages,
                    ttl_minutes=self.ttl_minutes
                )
                logger.info(f"Created new session: {session_id}")
            else:
                logger.debug(f"Retrieved existing session: {session_id}")

            return self.sessions[session_id]

    def add_user_message(self, session_id: str, content: str) -> None:
        """Add a user message to session."""
        session = self.get_or_create_session(session_id)
        session.add_message("user", content)
        logger.debug(f"Added user message to session {session_id}")

    def add_assistant_message(self, session_id: str, content: str) -> None:
        """Add an assistant message to session."""
        session = self.get_or_create_session(session_id)
        session.add_message("assistant", content)
        logger.debug(f"Added assistant message to session {session_id}")

    def get_session_history(self, session_id: str) -> List[Dict[str, str]]:
        """Get conversation history for a session."""
        session = self.get_or_create_session(session_id)
        return session.get_conversation_history()

    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        with self._lock:
            if session_id in self.sessions:
                del self.sessions[session_id]
                logger.info(f"Deleted session: {session_id}")
                return True
            return False

    def cleanup_expired_sessions(self) -> int:
        """Remove expired sessions. Returns number of sessions cleaned up."""
        with self._lock:
            expired_ids = [
                sid for sid, session in self.sessions.items()
                if session.is_expired()
            ]

            for session_id in expired_ids:
                del self.sessions[session_id]

            if expired_ids:
                logger.info(f"Cleaned up {len(expired_ids)} expired sessions")

            return len(expired_ids)

    def get_active_session_count(self) -> int:
        """Get number of active sessions."""
        return len(self.sessions)

    def _generate_session_id(self) -> str:
        """Generate a unique session ID."""
        return f"session-{uuid.uuid4().hex[:16]}"


# Global session manager instance
session_manager = SessionMemoryManager()
