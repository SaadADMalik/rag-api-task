# AI Agent Developer Interview Assignment - Implementation Plan

## Context
This is a comprehensive interview assignment requiring an end-to-end AI agent system with RAG capabilities, deployed to Azure. The goal is to demonstrate production-ready skills in:
- AI agent development with tool calling and memory
- RAG implementation with vector search
- Backend API development
- Azure cloud deployment
- DevOps best practices

**Key Solution Decision:** We'll use Azure's $200 free credit (30-day trial) which fully covers Azure OpenAI costs and deployment, satisfying all mandatory requirements while staying within budget.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        User/Client                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTPS
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Azure App Service (FastAPI)                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            AI Agent Engine                            │  │
│  │  • Decision Router (direct answer vs RAG)            │  │
│  │  • Tool Calling System                               │  │
│  │  • Session Memory Manager                            │  │
│  └──────┬───────────────────────────┬───────────────────┘  │
│         │                           │                       │
│         ▼                           ▼                       │
│  ┌─────────────┐           ┌──────────────────┐           │
│  │ Azure OpenAI│           │   RAG Pipeline   │           │
│  │  GPT-4o     │           │  • Embeddings    │           │
│  │             │           │  • Retrieval     │           │
│  └─────────────┘           └────────┬─────────┘           │
└──────────────────────────────────────┼──────────────────────┘
                                       │
                                       ▼
                        ┌──────────────────────────┐
                        │   Azure AI Search        │
                        │   (Vector Store)         │
                        │   • Document chunks      │
                        │   • Embeddings           │
                        │   • Metadata             │
                        └──────────────────────────┘
```

---

## Tech Stack & Justifications

### Core Technologies
- **Python 3.11+** - Latest stable with better performance
- **FastAPI** - Modern, fast, auto-documentation, async support
- **Azure OpenAI** - GPT-4o for agent + text-embedding-3-large for RAG
- **Azure AI Search** - Managed vector search, hybrid search capabilities
- **LangChain** - Agent framework, tool calling, memory management
- **Pydantic v2** - Data validation, settings management
- **Azure SDK** - Service integration, authentication

### DevOps & Deployment
- **Docker** - Containerization for consistent deployment
- **Azure Container Registry** - Private Docker image storage
- **Azure App Service (Linux)** - Container deployment with auto-scaling
- **Azure Key Vault** - Secrets management
- **Azure Application Insights** - Monitoring, logging, telemetry
- **GitHub Actions** - CI/CD pipeline (optional but impressive)

### Development Tools
- **Poetry** - Dependency management
- **pytest** - Unit and integration testing
- **Black + Ruff** - Code formatting and linting
- **pre-commit** - Git hooks for code quality
- **Postman/Bruno** - API testing collection

---

## Implementation Plan

### Phase 1: Project Scaffolding & Setup (Day 1)

**1.1 Project Structure**
```
whatsapp-analyzer/  (rename to ai-agent-rag-system)
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Settings & environment vars
│   ├── models.py               # Pydantic models
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── core.py            # Agent engine
│   │   ├── tools.py           # Tool definitions
│   │   ├── router.py          # Decision logic
│   │   └── memory.py          # Session management
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── embeddings.py      # Document processing
│   │   ├── retriever.py       # Vector search
│   │   └── indexer.py         # Index management
│   └── api/
│       ├── __init__.py
│       └── routes.py          # API endpoints
├── documents/                  # Sample documents (3-5 PDFs)
│   ├── company_policy.pdf
│   ├── hr_handbook.pdf
│   ├── it_security_guidelines.pdf
│   ├── expense_policy.pdf
│   └── remote_work_policy.pdf
├── tests/
│   ├── __init__.py
│   ├── test_agent.py
│   ├── test_rag.py
│   └── test_api.py
├── infrastructure/
│   ├── azure/
│   │   ├── main.bicep         # Infrastructure as Code
│   │   ├── parameters.json
│   │   └── deploy.sh
│   └── docker/
│       └── Dockerfile
├── scripts/
│   ├── setup_azure.sh         # Azure resource provisioning
│   ├── index_documents.py     # One-time document indexing
│   └── test_deployment.py     # Smoke tests
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── README.md
└── ARCHITECTURE.md
```

**1.2 Initial Setup**
- Initialize Poetry project with dependencies
- Set up pre-commit hooks (black, ruff, pytest)
- Create .env.example with all required variables
- Set up basic FastAPI skeleton with health check endpoint

### Phase 2: Sample Documents Creation (Day 1)

**2.1 Create 5 Realistic Company Policy Documents**
Generate professional PDF documents covering:
1. **Company Policy Handbook** - Leave policies, code of conduct, holidays
2. **HR Handbook** - Onboarding, performance reviews, benefits
3. **IT Security Guidelines** - Password policies, data handling, BYOD
4. **Expense & Travel Policy** - Reimbursement rules, approval processes
5. **Remote Work Policy** - Equipment, hours, communication expectations

Use realistic corporate language, multiple pages per document, proper formatting.

**Why these topics?** Common in enterprises, diverse enough to test retrieval quality, relatable for recruiters.

### Phase 3: RAG Pipeline Implementation (Day 2)

**3.1 Document Processing (`app/rag/embeddings.py`)**
- PDF text extraction using PyPDF2 or pdfplumber
- Text chunking strategy:
  - Chunk size: 1000 tokens with 200 token overlap
  - Preserve paragraph/section boundaries
  - Include metadata (filename, page number, section title)
- Generate embeddings using Azure OpenAI `text-embedding-3-large`

**3.2 Vector Store Setup (`app/rag/indexer.py`)**
- Create Azure AI Search index with schema:
  - `id`: Unique chunk identifier
  - `content`: Text content
  - `content_vector`: Embedding (1536 dimensions)
  - `metadata`: Document source, page, timestamp
- Implement hybrid search (vector + keyword)
- Batch upload chunks to index

**3.3 Retrieval System (`app/rag/retriever.py`)**
- Query embedding generation
- Top-K retrieval (K=5 by default, configurable)
- Re-ranking based on relevance score threshold (>0.7)
- Context formatting for LLM consumption

**3.4 Indexing Script (`scripts/index_documents.py`)**
- CLI script to process and index all documents
- Progress logging, error handling
- Idempotent (can re-run safely)

### Phase 4: AI Agent Development (Day 3)

**4.1 Agent Core (`app/agent/core.py`)**
- LangChain agent setup with Azure OpenAI GPT-4o
- System prompt engineering:
  ```
  You are an intelligent corporate assistant helping employees find information.
  You have access to company policy documents and can answer questions about them.

  Your decision process:
  1. If the question is general knowledge or greeting, answer directly
  2. If the question is about company policies/procedures, use the document_search tool
  3. Always cite your sources when using retrieved information
  4. If you don't find relevant information, say so honestly
  ```

**4.2 Tool Implementation (`app/agent/tools.py`)**
Implement at least 2 tools:

1. **`document_search`** (mandatory for RAG)
   - Input: User query string
   - Logic: Call RAG retriever, return relevant chunks
   - Output: Formatted context + source citations

2. **`calculate`** (bonus, shows multi-tool capability)
   - Input: Mathematical expression
   - Logic: Safe eval for basic calculations
   - Output: Calculated result

**4.3 Decision Router (`app/agent/router.py`)**
Smart routing logic to decide:
- **Direct answer**: Greetings, general knowledge, small talk
- **RAG search**: Questions containing policy keywords (leave, expense, security, etc.)
- Confidence scoring for transparency

**4.4 Session Memory (`app/agent/memory.py`)**
- In-memory session storage (dict with session_id keys)
- Store last 10 messages per session
- Conversation buffer for context
- TTL: 30 minutes (configurable)
- Cleanup job for expired sessions

### Phase 5: FastAPI Backend (Day 4)

**5.1 Core API (`app/main.py`)**
- FastAPI app initialization
- CORS middleware (configurable origins)
- Exception handlers (custom error responses)
- Startup/shutdown events (initialize Azure clients)
- Request logging middleware

**5.2 API Endpoints (`app/api/routes.py`)**

```python
POST /ask
Request:
{
  "query": "What is the leave policy for parental leave?",
  "session_id": "user-123-session-abc"  # Optional
}

Response:
{
  "answer": "According to our HR Handbook, parental leave policy provides...",
  "sources": [
    {
      "document": "hr_handbook.pdf",
      "page": 15,
      "relevance_score": 0.89
    }
  ],
  "decision": "rag_search",  # or "direct_answer"
  "session_id": "user-123-session-abc"
}

GET /health
Response:
{
  "status": "healthy",
  "azure_openai": "connected",
  "azure_search": "connected",
  "timestamp": "2026-04-06T12:00:00Z"
}

GET /docs
- Auto-generated Swagger UI

GET /sessions/{session_id}/history
Response:
{
  "session_id": "user-123-session-abc",
  "messages": [...]
}

DELETE /sessions/{session_id}
- Clear session memory
```

**5.3 Configuration (`app/config.py`)**
- Pydantic Settings for environment variables
- Azure OpenAI configuration
- Azure AI Search configuration
- Logging configuration
- Feature flags

**5.4 Models (`app/models.py`)**
- Request/response Pydantic models
- Type validation
- OpenAPI documentation strings

### Phase 6: Testing (Day 4-5)

**6.1 Unit Tests**
- `test_agent.py`: Agent decision logic, tool calling
- `test_rag.py`: Chunking, embedding, retrieval
- `test_api.py`: Endpoint validation, error handling

**6.2 Integration Tests**
- End-to-end query flow
- Session memory persistence
- Azure service connectivity

**6.3 API Testing Collection**
- Postman/Bruno collection with example requests
- Include in repository for easy testing

### Phase 7: Azure Deployment (Day 5-6)

**7.1 Azure Resource Provisioning**

Create Azure resources using Azure Portal or CLI:

1. **Azure OpenAI Service**
   - Deploy GPT-4o model
   - Deploy text-embedding-3-large model
   - Note endpoint and API key

2. **Azure AI Search**
   - Create search service (Basic tier sufficient)
   - Note endpoint and admin key

3. **Azure Container Registry**
   - Create ACR for Docker images
   - Enable admin access

4. **Azure App Service**
   - Create App Service Plan (Linux, B1 tier)
   - Configure container deployment from ACR
   - Set environment variables

5. **Azure Key Vault** (Bonus)
   - Store API keys and secrets
   - Grant App Service managed identity access

6. **Application Insights** (Bonus)
   - Create resource for monitoring
   - Connect to App Service

**7.2 Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

# Copy application
COPY app/ ./app/

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**7.3 Deployment Steps**
1. Build Docker image locally
2. Push to Azure Container Registry
3. Configure App Service to pull from ACR
4. Set environment variables in App Service
5. Run document indexing script (one-time)
6. Verify deployment with health check
7. Test `/ask` endpoint

**7.4 Environment Variables**
```
AZURE_OPENAI_ENDPOINT=https://your-openai.openai.azure.com/
AZURE_OPENAI_API_KEY=<from-key-vault>
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME=text-embedding-3-large
AZURE_SEARCH_ENDPOINT=https://your-search.search.windows.net
AZURE_SEARCH_ADMIN_KEY=<from-key-vault>
AZURE_SEARCH_INDEX_NAME=company-policies
LOG_LEVEL=INFO
ENABLE_CORS=true
CORS_ORIGINS=*
```

### Phase 8: Bonus Features (Day 6-7)

**8.1 Docker Compose (Local Development)**
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./app:/app/app
```

**8.2 Monitoring & Logging**
- Structured JSON logging
- Request/response logging
- Error tracking with stack traces
- Azure Application Insights integration:
  - Request telemetry
  - Dependency tracking (OpenAI, Search calls)
  - Custom metrics (RAG retrieval latency, agent decision distribution)
  - Alerts on error rates

**8.3 CI/CD Pipeline (GitHub Actions)**
```yaml
# .github/workflows/deploy.yml
name: Deploy to Azure
on:
  push:
    branches: [main]
jobs:
  build-and-deploy:
    - Run tests
    - Build Docker image
    - Push to ACR
    - Deploy to App Service
```

**8.4 Advanced Features**
- **Confidence scoring**: Return confidence level (0-1) for answers
- **Source citations**: Highlight exact snippets from documents
- **Query rewriting**: Improve user queries before RAG retrieval
- **Fallback handling**: Graceful degradation if Azure services are down
- **Rate limiting**: Prevent abuse (10 req/min per session)
- **Caching**: Cache frequent queries (Redis optional)

### Phase 9: Documentation (Day 7)

**9.1 README.md** (Comprehensive)
```markdown
# AI Agent with RAG - Corporate Policy Assistant

## Overview
Intelligent AI agent that answers questions about company policies using RAG.

## Architecture
[Diagram showing components]

## Tech Stack
- Python 3.11, FastAPI, LangChain
- Azure OpenAI (GPT-4o, text-embedding-3-large)
- Azure AI Search (vector store)
- Azure App Service (deployment)

## Features
✅ Smart routing (direct answer vs RAG)
✅ Tool calling (document search, calculator)
✅ Session-based memory
✅ Source citations
✅ RESTful API with auto-docs
✅ Docker containerization
✅ Azure Cloud deployment
✅ Monitoring & logging

## Local Setup
1. Prerequisites
2. Installation steps
3. Azure resource setup
4. Document indexing
5. Running locally

## Azure Deployment
1. Step-by-step deployment guide
2. Environment configuration
3. Verification

## API Documentation
Examples with curl commands

## Design Decisions
- Why Azure AI Search over FAISS
- GPT-4o vs GPT-4
- Chunking strategy rationale
- Memory implementation choice

## Limitations & Future Improvements
- Current: In-memory session storage
- Future: Redis for distributed sessions
- Current: Basic re-ranking
- Future: Cross-encoder re-ranking
- Scalability considerations

## Cost Estimation
Azure free tier covers testing period

## Testing
How to run tests

## Demo
Live URL: https://ai-agent-rag.azurewebsites.net
```

**9.2 ARCHITECTURE.md** (Deep Dive)
- Component breakdown
- Data flow diagrams
- Decision algorithms
- Performance considerations
- Security measures

**9.3 API Examples**
Create a `examples/` folder with:
- Sample curl commands
- Python client example
- JavaScript fetch example
- Postman collection

---

## Critical Files to Create

### Core Application
1. `app/main.py` - FastAPI application entry point
2. `app/config.py` - Configuration management
3. `app/models.py` - Pydantic models
4. `app/agent/core.py` - AI agent engine
5. `app/agent/tools.py` - Tool implementations
6. `app/agent/router.py` - Decision routing logic
7. `app/agent/memory.py` - Session management
8. `app/rag/embeddings.py` - Document processing
9. `app/rag/indexer.py` - Azure AI Search indexing
10. `app/rag/retriever.py` - Vector retrieval
11. `app/api/routes.py` - API endpoints

### Infrastructure
12. `Dockerfile` - Container definition
13. `docker-compose.yml` - Local development
14. `pyproject.toml` - Dependencies
15. `.env.example` - Environment template

### Documentation
16. `README.md` - Main documentation
17. `ARCHITECTURE.md` - Technical deep dive
18. `documents/` - 5 sample PDFs

### Testing
19. `tests/test_agent.py`
20. `tests/test_rag.py`
21. `tests/test_api.py`

### Scripts
22. `scripts/setup_azure.sh` - Resource provisioning
23. `scripts/index_documents.py` - Document indexing

---

## Verification & Testing Strategy

### Local Testing
1. **Unit Tests**: `pytest tests/ -v`
2. **Coverage**: `pytest tests/ --cov=app --cov-report=html`
3. **Manual API Testing**:
   ```bash
   # Start server
   uvicorn app.main:app --reload

   # Test direct answer
   curl -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"query": "Hello, how are you?"}'

   # Test RAG query
   curl -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the parental leave policy?"}'

   # Test with session
   curl -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"query": "How many days?", "session_id": "test-123"}'
   ```

### Azure Deployment Testing
1. **Health Check**: `curl https://your-app.azurewebsites.net/health`
2. **Smoke Tests**: Run `scripts/test_deployment.py`
3. **Load Testing**: Use Azure Load Testing (optional)
4. **Monitor Logs**: Check Application Insights

### Quality Checks
- [ ] All 5 tasks completed
- [ ] API accessible via public URL
- [ ] Source citations working
- [ ] Session memory persisting
- [ ] Error handling robust
- [ ] Documentation complete
- [ ] Tests passing (>80% coverage)
- [ ] Docker build successful
- [ ] Azure deployment verified
- [ ] Monitoring/logging active

---

## Key Impressive Elements

### 1. **Production-Ready Code Quality**
   - Proper project structure
   - Type hints everywhere
   - Exception handling
   - Logging at appropriate levels
   - Configuration management
   - Environment variable validation

### 2. **Advanced AI Features**
   - Smart routing logic (not just RAG for everything)
   - Multi-tool capability
   - Session memory with context
   - Source attribution
   - Confidence scoring

### 3. **Complete DevOps**
   - Dockerfile with health checks
   - Infrastructure as Code (optional Bicep)
   - Monitoring with Application Insights
   - Structured logging
   - CI/CD ready

### 4. **Excellent Documentation**
   - Clear README with diagrams
   - Architecture deep dive
   - Design decision rationale
   - Honest limitations discussion
   - API examples and Postman collection

### 5. **Above & Beyond**
   - More than 1 tool (2-3 tools)
   - Hybrid search (vector + keyword)
   - Re-ranking logic
   - Rate limiting
   - Comprehensive testing

---

## Timeline Breakdown

**Day 1**: Setup + Sample Documents (6-8 hours)
**Day 2**: RAG Pipeline (6-8 hours)
**Day 3**: AI Agent (6-8 hours)
**Day 4**: FastAPI + Testing (6-8 hours)
**Day 5-6**: Azure Deployment + Troubleshooting (8-12 hours)
**Day 7**: Bonus Features + Documentation (6-8 hours)

**Total**: ~45-55 hours across 7 days (comfortable pace with buffer)

---

## Success Criteria

✅ **Task 1**: AI agent accepts queries, routes to LLM or RAG, returns structured response
✅ **Task 2**: 5 sample PDFs embedded, stored in Azure AI Search, retrieval working
✅ **Task 3**: FastAPI backend with `/ask` endpoint, proper request/response models
✅ **Task 4**: Deployed to Azure App Service, publicly accessible URL
✅ **Task 5**: Comprehensive README with architecture, setup, design decisions

**Bonus**: Docker, monitoring, logging, tests, CI/CD foundation

---

## Risk Mitigation

**Risk**: Azure free trial setup issues
- **Mitigation**: Follow Azure setup guide carefully, verify $200 credit active

**Risk**: Document indexing fails
- **Mitigation**: Start with 1 small document, test pipeline, then scale to 5

**Risk**: Azure AI Search quota limits
- **Mitigation**: Basic tier allows sufficient capacity for assignment

**Risk**: Deployment delays
- **Mitigation**: Test Docker build locally first, provision Azure resources early

**Risk**: Complex RAG tuning
- **Mitigation**: Start with simple chunking (fixed size), optimize later if needed

---

This plan balances ambition with practicality, ensuring all mandatory requirements are met while incorporating impressive bonus features that demonstrate senior-level capabilities.
