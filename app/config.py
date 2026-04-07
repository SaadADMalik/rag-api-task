"""Configuration management using Pydantic Settings."""

import logging
from typing import Annotated, Any, List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application Settings
    APP_NAME: str = "AI Agent RAG System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"

    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    ENABLE_CORS: bool = True
    CORS_ORIGINS: Annotated[List[str], NoDecode] = Field(default_factory=lambda: ["*"])

    # Groq Settings
    GROQ_API_KEY: str = Field(..., description="Groq API key")
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    GROQ_TEMPERATURE: float = 0.2
    GROQ_MAX_TOKENS: int = 150
    GROQ_MAX_RETRIES: int = 0
    GROQ_TIMEOUT_SECONDS: float = 8.0

    # Embedding Settings
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Vector Store Settings
    VECTOR_STORE_TYPE: str = "faiss"
    FAISS_INDEX_PATH: str = "data/faiss_index"

    # RAG Settings
    RAG_CHUNK_SIZE: int = 800
    RAG_CHUNK_OVERLAP: int = 150
    RAG_TOP_K: int = 4
    RAG_RELEVANCE_THRESHOLD: float = 0.25
    RAG_ENABLE_HYBRID_SEARCH: bool = False

    # Agent Settings
    AGENT_MAX_ITERATIONS: int = 5
    AGENT_MEMORY_MAX_MESSAGES: int = 10
    AGENT_SESSION_TTL_MINUTES: int = 30
    AGENT_FORCE_RAG_MODE: bool = False
    AGENT_USE_CHAT_HISTORY: bool = False
    AGENT_CONTEXT_HISTORY_MESSAGES: int = 4
    AGENT_CONTEXT_DOCS: int = 3
    AGENT_MAX_ACTIVE_SESSIONS: int = 1000
    AGENT_SESSION_ID_MAX_LENGTH: int = 120
    AGENT_MESSAGE_MAX_CHARS: int = 4000
    AGENT_MAX_CONTEXT_CHARS: int = 8000
    AGENT_SLA_MODE_ENABLED: bool = True
    AGENT_LLM_TIMEOUT_SECONDS: float = 2.5
    AGENT_FALLBACK_MAX_POINTS: int = 5
    AGENT_MAX_CONCURRENT_LLM_REQUESTS: int = 2
    AGENT_LLM_MIN_INTERVAL_SECONDS: float = 0.35
    AGENT_RATE_LIMIT_COOLDOWN_SECONDS: float = 20.0
    AGENT_CACHE_INCLUDE_FALLBACK: bool = False

    # Feature Flags
    ENABLE_CALCULATOR_TOOL: bool = True
    ENABLE_CONFIDENCE_SCORING: bool = True
    ENABLE_QUERY_REWRITING: bool = False

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 10
    RATE_LIMIT_ONLY_ASK: bool = True

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any):
        """Parse CORS origins from comma-separated string."""
        if v == "*":
            return ["*"]
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        if isinstance(v, list):
            return [str(origin).strip() for origin in v if str(origin).strip()]
        raise ValueError("CORS_ORIGINS must be '*' or a comma-separated string/list")

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"LOG_LEVEL must be one of {valid_levels}")
        return v.upper()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


def setup_logging(log_level: str = "INFO") -> None:
    """Configure application logging."""
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


# Global settings instance
settings = Settings()
setup_logging(settings.LOG_LEVEL)
