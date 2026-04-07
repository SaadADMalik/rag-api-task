# AI Agent RAG System

Production-style FastAPI service for policy Q and A with:

- Dynamic routing between direct answer and RAG
- Deterministic tool-use path for calculator and explicit document search
- Local FAISS retrieval with sentence-transformers embeddings
- Session memory with TTL, bounded growth, and session ID hardening
- Response diagnostics for decision, fallback, and cache behavior

## 1) What This Project Solves

This service answers employee policy questions from indexed documents (for example: expense, travel, HR, and security policy).

When a question is policy-specific, the system retrieves relevant document chunks and answers from retrieved context.
When a question is general (for example greetings), it uses a direct answer path.

## 2) Architecture

High-level flow:

1. Client sends POST /ask with query and optional session_id.
2. Router chooses one of:
   - direct_answer
   - rag_search
   - tool_use
3. If rag_search:
   - retrieve top chunks from FAISS
   - build constrained policy prompt
   - generate answer with Groq model
4. If tool_use:
   - run calculator for arithmetic
   - run document search for explicit "search/find/lookup docs" requests
5. Apply response contract:
   - plain text normalization
   - optional source tail
   - bounded answer length
6. Return structured response with decision, sources, fallback fields, and timing.

## 3) Tech Stack

- Python 3.11+
- FastAPI
- Pydantic / pydantic-settings
- LangChain ecosystem
- Groq chat model integration
- sentence-transformers embeddings
- FAISS local vector store
- PyPDF2 for PDF extraction
- pytest for tests

## 4) Project Layout

- app: API, agent, and RAG modules
- documents: source policy PDFs
- scripts: indexing utilities
- tests: unit tests
- data/faiss_index: persisted FAISS index files

## 5) Prerequisites

- Python installed (recommended 3.11+)
- Groq API key

## 6) Setup

### Windows PowerShell

1. Create and activate virtual environment

   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

2. Install dependencies

   pip install -e .

3. Configure environment

   - Copy .env.example to .env
   - Set GROQ_API_KEY in .env

## 7) Generate or Refresh Documents

If needed, regenerate PDFs using scripts in the repository root and documents folder.

Then index all PDFs:

py scripts\index_documents.py

What this does:

- backs up existing FAISS index
- rebuilds index from all PDFs in documents
- restores backup automatically if indexing fails

## 8) Run the API

py -m uvicorn app.main:app --host 127.0.0.1 --port 8000

API docs:

- http://127.0.0.1:8000/docs

## 9) API Contract

### POST /ask

Request JSON:

- query: string, required, 1..1000 chars
- session_id: optional string, pattern ^[a-zA-Z0-9._:-]+$, max 120 chars

Response JSON fields:

- answer: plain text answer
- source: list of source document names (Task 3 compatibility)
- sources: list of source documents with relevance and snippets
- decision: direct_answer | rag_search | tool_use
- session_id: effective session identifier
- confidence: optional confidence score
- processing_time_ms: elapsed processing time
- fallback_used: true if fallback path used
- fallback_reason: reason for fallback when present
- cache_hit: true when response was served from in-memory cache

### GET /health

Returns service status and dependency state summary.

### Session endpoints

- GET /sessions/{session_id}/history
- DELETE /sessions/{session_id}
- GET /sessions/stats

## 10) Testing

Run focused tests:

& "d:/Whatsapp analyzer/.venv/Scripts/python.exe" -m pytest -q tests\test_router.py tests\test_memory.py tests\test_core_tools.py tests\test_retriever.py

Run all tests:

& "d:/Whatsapp analyzer/.venv/Scripts/python.exe" -m pytest

## 11) Operational Notes

- First startup can be slower because embedding model loading is CPU-heavy.
- Fallback can occur even when API is healthy if provider rate limits trigger cooldown.
- 429 responses with scope api_gateway indicate gateway rate limiting, not model failure.

## 12) Troubleshooting

1. Import errors in tests
   - install missing dependencies into the active environment
2. No FAISS index found
   - run py scripts\index_documents.py
3. Frequent fallback under load
   - reduce request burst rate
   - tune AGENT_LLM_MIN_INTERVAL_SECONDS and AGENT_RATE_LIMIT_COOLDOWN_SECONDS
4. Validation error on session_id
   - use only letters, numbers, dot, underscore, colon, and hyphen

## 13) Current Status Snapshot

Completed implementation milestones:

- dynamic query routing
- real tool-use path
- finalized prompt and response contract
- hardened session memory behavior
- stabilized ingestion pipeline
- improved retrieval relevance
- locked API schema
- added automated tests and fixtures

## 14) Azure Deployment (Groq)

You can deploy this project to Azure App Service without Docker.
Dockerized deployment is optional and is a bonus item in the assignment, not a mandatory requirement.

### Option A: Deploy Without Docker (Recommended first)

1. Install and sign in to Azure CLI

   az login

2. Create resource group and App Service plan

   az group create --name rg-ai-agent-rag --location eastus
   az appservice plan create --name plan-ai-agent-rag --resource-group rg-ai-agent-rag --sku B1 --is-linux

3. Create a Linux Python web app

   az webapp create --name <unique-app-name> --resource-group rg-ai-agent-rag --plan plan-ai-agent-rag --runtime "PYTHON|3.11"

4. Configure runtime app settings

   az webapp config appsettings set --name <unique-app-name> --resource-group rg-ai-agent-rag --settings GROQ_API_KEY="<your-key>" GROQ_MODEL="llama-3.1-8b-instant" LOG_LEVEL="INFO" ENABLE_CORS="true" CORS_ORIGINS="*" FAISS_INDEX_PATH="data/faiss_index"

5. Set startup command

   az webapp config set --name <unique-app-name> --resource-group rg-ai-agent-rag --startup-file "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

6. Export Python dependencies for App Service build

   poetry export -f requirements.txt --output requirements.txt --without-hashes

7. Deploy source code (zip deploy)

   Compress-Archive -Path app,documents,scripts,pyproject.toml,requirements.txt,README.md,.env.example -DestinationPath deploy.zip -Force
   az webapp deploy --name <unique-app-name> --resource-group rg-ai-agent-rag --src-path deploy.zip --type zip

8. Verify public URL

   https://<unique-app-name>.azurewebsites.net/health
   https://<unique-app-name>.azurewebsites.net/docs

### Option B: Deploy With Docker (Optional)

You can use the existing Dockerfile and docker-compose setup to deploy containerized to Azure Web App for Containers.
This is optional and useful when you want stricter runtime parity.

## 15) Design Decisions

1. Dynamic routing first, retrieval only when needed
   Reduces cost/latency for simple queries.
2. Deterministic tool path for calculator and explicit document search
   Keeps behavior predictable for interview evaluation.
3. FAISS local vector store
   Fast local setup without requiring managed vector infra.
4. Dual response fields (`source` and `sources`)
   `source` satisfies assignment Task 3 format, while `sources` retains richer metadata.
5. Session memory with TTL and bounded payload sizes
   Prevents unbounded memory growth.

## 16) Limitations and Future Improvements

Limitations:

1. Uses local FAISS files, not a managed cloud vector database.
2. Session memory is in-process; it is not shared across multiple instances.
3. Health check is basic and does not yet run deep dependency probes.

Future improvements:

1. Add Redis-backed distributed memory for multi-instance deployments.
2. Add CI/CD pipeline for automated Azure deployment.
3. Add API integration tests for `app/main.py` and `app/api/routes.py` to improve coverage.
4. Add Azure Monitor / Application Insights telemetry dashboards.
