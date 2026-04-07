"""Main FastAPI application for AI Agent RAG System."""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import logging
import time
from datetime import datetime

from app.config import settings
from app.api.routes import router
from app.agent.memory import session_manager
from app.models import ErrorResponse

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.
    """
    # Startup
    logger.info("=" * 60)
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Log level: {settings.LOG_LEVEL}")
    logger.info("=" * 60)

    # Initialize services
    logger.info("Initializing services...")
    logger.info(f"Groq model: {settings.GROQ_MODEL}")
    logger.info(f"Embedding model: {settings.EMBEDDING_MODEL_NAME}")
    logger.info(f"Vector store: {settings.VECTOR_STORE_TYPE} ({settings.FAISS_INDEX_PATH})")
    logger.info(f"Session memory: max_messages={settings.AGENT_MEMORY_MAX_MESSAGES}, ttl={settings.AGENT_SESSION_TTL_MINUTES}min")

    logger.info("Application startup complete!")

    yield

    # Shutdown
    logger.info("Shutting down application...")
    logger.info(f"Active sessions: {session_manager.get_active_session_count()}")
    logger.info("Cleanup complete. Goodbye!")


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "AI Agent with RAG capabilities for answering questions about company policies. "
        "The agent can search through policy documents, perform calculations, and maintain conversation context."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# ============================================================================
# Middleware
# ============================================================================

if settings.ENABLE_CORS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info(f"CORS enabled for origins: {settings.CORS_ORIGINS}")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and add request timing."""
    start_time = time.time()

    # Generate request ID
    request_id = f"{int(start_time * 1000)}"

    # Log request
    logger.info(
        f"Request started: {request.method} {request.url.path} "
        f"[id: {request_id}]"
    )

    # Process request
    response = await call_next(request)

    # Calculate duration
    duration_ms = (time.time() - start_time) * 1000

    # Log response
    logger.info(
        f"Request completed: {request.method} {request.url.path} "
        f"[id: {request_id}] [status: {response.status_code}] "
        f"[duration: {duration_ms:.2f}ms]"
    )

    # Add custom headers
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{duration_ms:.2f}ms"

    return response


# ============================================================================
# Exception Handlers
# ============================================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors."""
    logger.warning(f"Validation error: {exc.errors()}")

    error_response = ErrorResponse(
        error="ValidationError",
        message="Invalid request data",
        detail={
            "errors": exc.errors(),
            "body": exc.body
        },
        timestamp=datetime.utcnow()
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)

    error_response = ErrorResponse(
        error="InternalServerError",
        message="An unexpected error occurred",
        detail={"error_type": type(exc).__name__} if settings.DEBUG else None,
        timestamp=datetime.utcnow()
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.dict()
    )


# ============================================================================
# Routes
# ============================================================================

# Include API routes
app.include_router(router, tags=["AI Agent"])


@app.get(
    "/",
    tags=["Root"],
    summary="Root endpoint",
    description="Get basic API information"
)
async def root():
    """Root endpoint returning basic API info."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "docs": "/docs",
        "health": "/health"
    }


# ============================================================================
# Run Application
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
