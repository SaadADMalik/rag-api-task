"""Session memory management for conversation context."""

from typing import Dict, List, Optional
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
import threading
import logging
import uuid
import re

from app.config import settings

logger = logging.getLogger(__name__)


@dataclass
class Message:
    """Conversation message."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime


class Session:
    """Session with conversation history."""

    def __init__(
        self,
        session_id: str,
        max_messages: int = 10,
        ttl_minutes: int = 30,
        max_message_chars: int = 4000,
    ):
        self.session_id = session_id
        self.messages: List[Message] = []
        self.max_messages = max_messages
        self.ttl_minutes = ttl_minutes
        self.max_message_chars = max_message_chars
        self.created_at = datetime.now(timezone.utc)
        self.last_accessed = datetime.now(timezone.utc)

    def touch(self) -> None:
        """Refresh last-accessed timestamp."""
        self.last_accessed = datetime.now(timezone.utc)

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the session."""
        normalized_role = (role or "").strip().lower()
        if normalized_role not in {"user", "assistant"}:
            normalized_role = "user"

        normalized_content = (content or "").strip()
        if not normalized_content:
            normalized_content = "[empty message]"

        if len(normalized_content) > self.max_message_chars:
            normalized_content = normalized_content[: self.max_message_chars].rstrip() + "..."

        self.messages.append(Message(
            role=normalized_role,
            content=normalized_content,
            timestamp=datetime.now(timezone.utc)
        ))
        self.touch()

        # Keep only the last max_messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get formatted conversation history for LLM."""
        self.touch()
        return [
            {"role": msg.role, "content": msg.content}
            for msg in self.messages
        ]

    def is_expired(self) -> bool:
        """Check if session has expired."""
        expiry_time = self.last_accessed + timedelta(minutes=self.ttl_minutes)
        return datetime.now(timezone.utc) > expiry_time

    def get_message_count(self) -> int:
        """Get total number of messages in session."""
        return len(self.messages)


class SessionMemoryManager:
    """Manages multiple user sessions with TTL-based cleanup."""

    def __init__(
        self,
        max_messages_per_session: int = 10,
        session_ttl_minutes: int = 30,
        max_active_sessions: int = 1000,
        max_session_id_length: int = 120,
        max_message_chars: int = 4000,
    ):
        self.sessions: Dict[str, Session] = {}
        self.max_messages = max_messages_per_session
        self.ttl_minutes = session_ttl_minutes
        self.max_active_sessions = max_active_sessions
        self.max_session_id_length = max_session_id_length
        self.max_message_chars = max_message_chars
        self._lock = threading.Lock()
        logger.info(
            f"SessionMemoryManager initialized: "
            f"max_messages={max_messages_per_session}, ttl={session_ttl_minutes}min"
        )

    def _normalize_session_id(self, session_id: Optional[str]) -> Optional[str]:
        """Sanitize external session IDs to avoid unbounded/invalid keys."""
        if session_id is None:
            return None

        value = str(session_id).strip()
        if not value:
            return None

        value = value[: self.max_session_id_length]
        # Keep a conservative set of ID-safe characters.
        value = re.sub(r"[^a-zA-Z0-9._:-]", "", value)

        return value or None

    def _evict_one_if_needed(self) -> None:
        """Evict one session when over capacity, preferring expired then least-recently-used."""
        if len(self.sessions) < self.max_active_sessions:
            return

        expired_ids = [sid for sid, s in self.sessions.items() if s.is_expired()]
        if expired_ids:
            sid = expired_ids[0]
            self.sessions.pop(sid, None)
            logger.info("Evicted expired session due to capacity: %s", sid)
            return

        oldest_id = min(self.sessions, key=lambda sid: self.sessions[sid].last_accessed)
        self.sessions.pop(oldest_id, None)
        logger.warning("Evicted least-recently-used session due to capacity: %s", oldest_id)

    def _get_or_create_session_locked(self, session_id: Optional[str]) -> Session:
        """Get existing session or create new one. Lock must be held by caller."""
        normalized_session_id = self._normalize_session_id(session_id)
        if normalized_session_id is None:
            normalized_session_id = self._generate_session_id()

        existing = self.sessions.get(normalized_session_id)
        if existing is not None:
            if existing.is_expired():
                self.sessions.pop(normalized_session_id, None)
                logger.info("Expired session recreated: %s", normalized_session_id)
            else:
                existing.touch()
                logger.debug("Retrieved existing session: %s", normalized_session_id)
                return existing

        self._evict_one_if_needed()
        session = Session(
            session_id=normalized_session_id,
            max_messages=self.max_messages,
            ttl_minutes=self.ttl_minutes,
            max_message_chars=self.max_message_chars,
        )
        self.sessions[normalized_session_id] = session
        logger.info("Created new session: %s", normalized_session_id)
        return session

    def get_or_create_session(self, session_id: Optional[str] = None) -> Session:
        """Get existing session or create new one."""
        with self._lock:
            return self._get_or_create_session_locked(session_id)

    def add_user_message(self, session_id: str, content: str) -> None:
        """Add a user message to session."""
        with self._lock:
            session = self._get_or_create_session_locked(session_id)
            session.add_message("user", content)
            logger.debug("Added user message to session %s", session.session_id)

    def add_assistant_message(self, session_id: str, content: str) -> None:
        """Add an assistant message to session."""
        with self._lock:
            session = self._get_or_create_session_locked(session_id)
            session.add_message("assistant", content)
            logger.debug("Added assistant message to session %s", session.session_id)

    def get_session_history(self, session_id: str) -> List[Dict[str, str]]:
        """Get conversation history for a session."""
        with self._lock:
            session = self._get_or_create_session_locked(session_id)
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
        self.cleanup_expired_sessions()
        with self._lock:
            return len(self.sessions)

    def _generate_session_id(self) -> str:
        """Generate a unique session ID."""
        return f"session-{uuid.uuid4().hex[:16]}"


# Global session manager instance
session_manager = SessionMemoryManager(
    max_messages_per_session=settings.AGENT_MEMORY_MAX_MESSAGES,
    session_ttl_minutes=settings.AGENT_SESSION_TTL_MINUTES,
    max_active_sessions=settings.AGENT_MAX_ACTIVE_SESSIONS,
    max_session_id_length=settings.AGENT_SESSION_ID_MAX_LENGTH,
    max_message_chars=settings.AGENT_MESSAGE_MAX_CHARS,
)
