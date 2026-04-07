import asyncio
import logging
import re
import time
from typing import Any, Dict, List, Optional

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from app.config import settings
from app.agent.memory import session_manager
from app.agent.prompts import DIRECT_SYSTEM_PROMPT, RAG_SYSTEM_PROMPT
from app.agent.router import decision_router
from app.agent.tools import create_tools
from app.rag.retriever import retriever

logger = logging.getLogger(__name__)

FALLBACK_DOC_SCORE_MARGIN = 0.04
FALLBACK_MAX_DOCS = 2


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
        self._tools = {tool.name: tool for tool in create_tools()}
        self._response_cache: Dict[str, Dict[str, Any]] = {}
        self._cache_ttl_seconds = 1800
        self._llm_semaphore = asyncio.Semaphore(max(1, settings.AGENT_MAX_CONCURRENT_LLM_REQUESTS))
        self._llm_spacing_lock = asyncio.Lock()
        self._next_llm_call_at = 0.0
        self._provider_cooldown_until = 0.0
        logger.info("AIAgent initialized successfully with tools: %s", sorted(self._tools.keys()))

    def _initialize_llm(self) -> ChatGroq:
        """Initialize Groq LLM."""
        logger.info("Initializing Groq LLM...")

        llm = ChatGroq(
            model=settings.GROQ_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=settings.GROQ_TEMPERATURE,
            max_tokens=settings.GROQ_MAX_TOKENS,
            max_retries=settings.GROQ_MAX_RETRIES,
            timeout=settings.GROQ_TIMEOUT_SECONDS,
        )

        logger.info(
            "Groq initialized: model=%s, temp=%s",
            settings.GROQ_MODEL,
            settings.GROQ_TEMPERATURE,
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
        logger.info("Processing query: '%s' (session: %s)", query, session_id)

        session = session_manager.get_or_create_session(session_id)
        actual_session_id = session.session_id
        session_manager.add_user_message(actual_session_id, query)

        tool_call = self._detect_tool_call(query)
        if tool_call:
            decision, confidence = "tool_use", 1.0
            logger.info("Decision: tool_use (tool=%s)", tool_call["name"])
        else:
            decision, confidence = decision_router.decide(query)

        logger.info("Decision: %s (confidence: %.2f)", decision, confidence)

        try:
            cache_key = self._build_cache_key(query, decision)
            cached = self._get_cached_response(cache_key)
            if cached is not None:
                result = {
                    "answer": cached["answer"],
                    "sources": cached["sources"],
                    "decision": decision,
                    "session_id": actual_session_id,
                    "confidence": confidence if settings.ENABLE_CONFIDENCE_SCORING else None,
                    "fallback_used": cached.get("fallback_used", False),
                    "fallback_reason": cached.get("fallback_reason"),
                    "cache_hit": True,
                }
                session_manager.add_assistant_message(actual_session_id, result["answer"])
                logger.info("Served response from in-memory cache")
                return result

            fallback_used = False
            fallback_reason = None
            cache_hit = False

            history = session_manager.get_session_history(actual_session_id)
            chat_history = self._format_chat_history(history)[:-1]
            if settings.AGENT_USE_CHAT_HISTORY:
                chat_history = chat_history[-settings.AGENT_CONTEXT_HISTORY_MESSAGES:]
            else:
                chat_history = []

            sources: List[Dict[str, Any]] = []
            context_docs: List[Dict[str, Any]] = []

            if decision == "tool_use":
                tool_result = self._execute_tool_call(tool_call)
                answer = tool_result["answer"]
                sources = tool_result.get("sources", [])
            else:
                if decision == "rag_search":
                    documents = retriever.retrieve(query)

                    if not documents:
                        answer = self._apply_response_contract(
                            answer=(
                                "I could not find enough relevant policy information in the indexed documents "
                                "to answer this question confidently. Please contact HR or IT for clarification."
                            ),
                            decision=decision,
                            sources=[],
                            fallback_used=True,
                            fallback_reason="no_documents",
                        )
                        session_manager.add_assistant_message(actual_session_id, answer)
                        return {
                            "answer": answer,
                            "sources": [],
                            "decision": decision,
                            "session_id": actual_session_id,
                            "confidence": confidence if settings.ENABLE_CONFIDENCE_SCORING else None,
                            "fallback_used": True,
                            "fallback_reason": "no_documents",
                            "cache_hit": cache_hit,
                        }

                    context_docs = documents[:settings.AGENT_CONTEXT_DOCS]
                    context = retriever.format_context(context_docs)
                    context = self._trim_context(context)
                    sources = retriever.get_sources_summary(documents)

                    logger.info(
                        "RAG context prepared [docs=%s] [sources=%s] [context_chars=%s]",
                        len(context_docs),
                        len(sources),
                        len(context),
                    )

                    messages = [
                        SystemMessage(content=RAG_SYSTEM_PROMPT),
                        *chat_history,
                        HumanMessage(
                            content=(
                                f"User question: {query}\n\n"
                                f"Retrieved context:\n{context}"
                            )
                        ),
                    ]
                else:
                    logger.info("Direct-answer path selected (no document retrieval)")
                    messages = [
                        SystemMessage(content=DIRECT_SYSTEM_PROMPT),
                        *chat_history,
                        HumanMessage(content=query),
                    ]

                if self._is_provider_in_cooldown():
                    fallback_used = True
                    fallback_reason = "provider_cooldown"
                    if decision == "rag_search":
                        answer = self._build_extractive_fallback(query, context_docs)
                    else:
                        answer = self._build_direct_fallback(query)
                    logger.warning(
                        "Provider cooldown active (%.2fs remaining). Using fallback without LLM call.",
                        self._provider_cooldown_remaining_seconds(),
                    )
                else:
                    try:
                        llm_response = await self._invoke_llm(messages)
                        answer = getattr(llm_response, "content", str(llm_response))

                    except asyncio.TimeoutError:
                        fallback_used = True
                        fallback_reason = (
                            "rate_limited_timeout"
                            if self._is_provider_in_cooldown()
                            else "llm_timeout"
                        )
                        logger.warning(
                            "LLM timeout after %.2fs. Using extractive fallback.",
                            settings.AGENT_LLM_TIMEOUT_SECONDS,
                        )
                        if decision == "rag_search":
                            answer = self._build_extractive_fallback(query, context_docs)
                        else:
                            answer = self._build_direct_fallback(query)

                    except Exception as llm_error:
                        fallback_used = True
                        if self._is_rate_limit_error(llm_error):
                            self._activate_provider_cooldown(str(llm_error))
                            fallback_reason = "provider_rate_limited"
                        else:
                            fallback_reason = "llm_error"
                        logger.warning(
                            "LLM generation failed (%s). Using extractive fallback.",
                            str(llm_error),
                        )
                        if decision == "rag_search":
                            answer = self._build_extractive_fallback(query, context_docs)
                        else:
                            answer = self._build_direct_fallback(query)

            answer = self._apply_response_contract(
                answer=answer,
                decision=decision,
                sources=sources,
                fallback_used=fallback_used,
                fallback_reason=fallback_reason,
            )

            session_manager.add_assistant_message(actual_session_id, answer)
            should_cache = (not fallback_used) or settings.AGENT_CACHE_INCLUDE_FALLBACK
            if should_cache:
                self._set_cached_response(
                    cache_key,
                    answer,
                    sources,
                    fallback_used=fallback_used,
                    fallback_reason=fallback_reason,
                )

            result = {
                "answer": answer,
                "sources": sources,
                "decision": decision,
                "session_id": actual_session_id,
                "confidence": confidence if settings.ENABLE_CONFIDENCE_SCORING else None,
                "fallback_used": fallback_used,
                "fallback_reason": fallback_reason,
                "cache_hit": cache_hit,
            }

            logger.info("Query processed successfully for session %s", actual_session_id)
            return result

        except Exception as e:
            logger.error("Error processing query: %s", str(e), exc_info=True)
            return {
                "answer": f"I apologize, but I encountered an error: {str(e)}",
                "sources": [],
                "decision": decision,
                "session_id": actual_session_id,
                "confidence": 0.0,
                "fallback_used": True,
                "fallback_reason": "agent_exception",
                "cache_hit": False,
            }

    @staticmethod
    def _build_cache_key(query: str, decision: str) -> str:
        """Build stable cache key from normalized query text."""
        normalized = re.sub(r"\s+", " ", (query or "").strip().lower())
        return f"{decision}:{normalized}"

    def _detect_tool_call(self, query: str) -> Optional[Dict[str, str]]:
        """Detect whether a deterministic tool call should handle this query."""
        expression = self._extract_calculator_expression(query)
        if expression and settings.ENABLE_CALCULATOR_TOOL:
            return {"name": "calculator", "input": expression}

        normalized = (query or "").strip()
        doc_match = re.match(
            r"^(?:search|find|lookup)\s+(?:the\s+)?(?:documents|docs|policy|policies)\s*(?:for|about)?\s*(.+)$",
            normalized,
            flags=re.IGNORECASE,
        )
        if doc_match:
            search_query = doc_match.group(1).strip().rstrip("?.!")
            if search_query:
                return {"name": "document_search", "input": search_query}

        return None

    @staticmethod
    def _extract_calculator_expression(query: str) -> Optional[str]:
        """Extract safe calculator expression from natural query text."""
        raw = (query or "").strip()
        if not raw:
            return None

        lowered = raw.lower()
        if any(
            term in lowered
            for term in ("policy", "handbook", "expense", "reimbursement", "leave", "security")
        ):
            return None

        candidate = raw
        for pattern in (
            r"^\s*(?:calculate|compute|evaluate|eval|solve)\s*[:\-]?\s*(.+)$",
            r"^\s*(?:what is|what's)\s+(.+)$",
        ):
            match = re.match(pattern, candidate, flags=re.IGNORECASE)
            if match:
                candidate = match.group(1).strip()
                break

        candidate = candidate.rstrip("?.!")
        normalized = f" {candidate.lower()} "

        replacements = (
            (" multiplied by ", " * "),
            (" times ", " * "),
            (" x ", " * "),
            (" divided by ", " / "),
            (" over ", " / "),
            (" plus ", " + "),
            (" minus ", " - "),
            (" modulo ", " % "),
            (" mod ", " % "),
        )
        for src, dest in replacements:
            normalized = normalized.replace(src, dest)

        candidate = re.sub(r"\s+", " ", normalized).strip()

        if not re.search(r"\d", candidate):
            return None
        if not re.search(r"[\+\-\*\/%]", candidate):
            return None
        if not re.fullmatch(r"[\d\+\-\*\/\(\)\.\s%]+", candidate):
            return None

        return candidate

    def _execute_tool_call(self, tool_call: Optional[Dict[str, str]]) -> Dict[str, Any]:
        """Execute a detected tool call and return answer plus structured sources."""
        if not tool_call:
            return {
                "answer": "I could not determine which tool to execute.",
                "sources": [],
            }

        tool_name = tool_call.get("name", "")
        tool_input = tool_call.get("input", "")
        tool = self._tools.get(tool_name)

        if tool is None:
            return {
                "answer": f"Requested tool '{tool_name}' is not available.",
                "sources": [],
            }

        try:
            if tool_name == "document_search":
                documents = retriever.retrieve(tool_input)
                if not documents:
                    return {
                        "answer": (
                            "I could not find relevant policy content for that search query. "
                            "Please refine the search terms."
                        ),
                        "sources": [],
                    }

                sources = retriever.get_sources_summary(documents)
                lines = ["Top matches from policy documents:"]
                for idx, doc in enumerate(documents[:3], 1):
                    snippet = re.sub(r"\s+", " ", doc.get("content", "")).strip()
                    if len(snippet) > 220:
                        snippet = f"{snippet[:220].rstrip()}..."
                    source_ref = self._format_source_ref(doc.get("document", "unknown"), doc.get("page"))
                    lines.append(f"{idx}. {snippet} (source: {source_ref})")

                logger.info("Tool executed [tool=%s] [input=%s]", tool_name, tool_input)
                return {
                    "answer": "\n".join(lines),
                    "sources": sources,
                }

            output = tool.run(tool_input)
            text = (str(output) if output is not None else "").strip()
            logger.info("Tool executed [tool=%s] [input=%s]", tool_name, tool_input)

            if tool_name == "calculator" and text and not text.lower().startswith("error"):
                text = f"{tool_input} = {text}"

            return {
                "answer": text or "The tool completed but returned no output.",
                "sources": [],
            }

        except Exception as error:
            logger.error("Tool execution failed [tool=%s]: %s", tool_name, str(error), exc_info=True)
            return {
                "answer": f"I encountered an error while running the {tool_name} tool: {str(error)}",
                "sources": [],
            }

    async def _invoke_llm(self, messages: List[Any]) -> Any:
        """Invoke LLM with concurrency guard, pacing, and optional SLA timeout."""
        async with self._llm_semaphore:
            await self._enforce_llm_pacing()
            started = time.time()
            if settings.AGENT_SLA_MODE_ENABLED:
                response = await asyncio.wait_for(
                    self.llm.ainvoke(messages),
                    timeout=settings.AGENT_LLM_TIMEOUT_SECONDS,
                )
            else:
                response = await self.llm.ainvoke(messages)

            elapsed_ms = (time.time() - started) * 1000
            logger.info("LLM invoke success [duration=%.2fms]", elapsed_ms)
            return response

    async def _enforce_llm_pacing(self) -> None:
        """Apply a minimum gap between LLM calls to reduce provider burst limits."""
        min_interval = max(0.0, settings.AGENT_LLM_MIN_INTERVAL_SECONDS)
        if min_interval <= 0:
            return

        async with self._llm_spacing_lock:
            now = time.time()
            delay = self._next_llm_call_at - now
            if delay > 0:
                await asyncio.sleep(delay)
                now = time.time()

            self._next_llm_call_at = max(self._next_llm_call_at, now) + min_interval

    def _activate_provider_cooldown(self, error_message: str) -> None:
        """Start provider cooldown window after rate-limit errors."""
        cooldown_for = max(1.0, settings.AGENT_RATE_LIMIT_COOLDOWN_SECONDS)
        until = time.time() + cooldown_for
        self._provider_cooldown_until = max(self._provider_cooldown_until, until)
        logger.warning(
            "Provider rate limit detected. Cooling down LLM calls for %.2fs. Error: %s",
            cooldown_for,
            error_message,
        )

    def _is_provider_in_cooldown(self) -> bool:
        """Return whether LLM provider cooldown is active."""
        return time.time() < self._provider_cooldown_until

    def _provider_cooldown_remaining_seconds(self) -> float:
        """Return remaining provider cooldown time in seconds."""
        return max(0.0, self._provider_cooldown_until - time.time())

    @staticmethod
    def _is_rate_limit_error(error: Exception) -> bool:
        """Detect provider rate-limit failures from exception text."""
        text = str(error).lower()
        markers = ["429", "too many requests", "rate limit", "rate_limited"]
        return any(marker in text for marker in markers)

    def _get_cached_response(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Return cached response if still valid."""
        item = self._response_cache.get(cache_key)
        if not item:
            return None

        if time.time() > item["expires_at"]:
            self._response_cache.pop(cache_key, None)
            return None

        return {
            "answer": item["answer"],
            "sources": item["sources"],
            "fallback_used": item.get("fallback_used", False),
            "fallback_reason": item.get("fallback_reason"),
        }

    def _set_cached_response(
        self,
        cache_key: str,
        answer: str,
        sources: List[Dict[str, Any]],
        fallback_used: bool,
        fallback_reason: Optional[str],
    ) -> None:
        """Store response in cache with TTL."""
        self._response_cache[cache_key] = {
            "answer": answer,
            "sources": sources,
            "fallback_used": fallback_used,
            "fallback_reason": fallback_reason,
            "expires_at": time.time() + self._cache_ttl_seconds,
        }

    def _sanitize_answer_text(self, answer: str) -> str:
        """Normalize output to plain text and strip common markdown markers."""
        text = (answer or "").strip()
        text = text.replace("\r\n", "\n")

        text = re.sub(r"\*\*(.*?)\*\*", r"\1", text, flags=re.DOTALL)
        text = re.sub(r"__(.*?)__", r"\1", text, flags=re.DOTALL)
        text = re.sub(r"`([^`]*)`", r"\1", text)
        text = re.sub(r"(?m)^\s{0,3}#{1,6}\s*", "", text)
        text = re.sub(r"(?m)^\s*[\*\-\u2022]\s+", "", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def _apply_response_contract(
        self,
        answer: str,
        decision: str,
        sources: List[Dict[str, Any]],
        fallback_used: bool,
        fallback_reason: Optional[str],
    ) -> str:
        """Apply a consistent plain-text response contract across all decisions."""
        text = self._sanitize_answer_text(answer)
        if not text:
            text = "I could not produce a response. Please try again."

        if fallback_used and fallback_reason:
            reason_text = fallback_reason.replace("_", " ")
            if reason_text not in text.lower():
                text = f"Note: fallback mode was used due to {reason_text}.\n{text}"

        if decision in {"rag_search", "tool_use"} and sources and "source" not in text.lower():
            text = f"{text}\nSources: {self._format_sources_tail(sources)}"

        max_chars = 1200 if decision == "rag_search" else (900 if decision == "tool_use" else 450)
        if len(text) > max_chars:
            text = text[:max_chars].rstrip()
            if text and text[-1] not in ".!?":
                text += "..."

        return text

    @staticmethod
    def _format_sources_tail(sources: List[Dict[str, Any]], max_items: int = 3) -> str:
        """Format compact source tail for contract enforcement."""
        items = []
        for source in sources[:max_items]:
            doc = source.get("document", "unknown")
            page = source.get("page")
            items.append(f"{doc} p.{page}" if page else str(doc))

        return "; ".join(items)

    def _trim_context(self, context: str) -> str:
        """Cap context length before sending to model."""
        max_chars = max(500, settings.AGENT_MAX_CONTEXT_CHARS)
        if len(context) <= max_chars:
            return context

        trimmed = context[:max_chars]
        if "\n---\n" in trimmed:
            trimmed = trimmed.rsplit("\n---\n", 1)[0]

        logger.warning(
            "Context trimmed before LLM call [original_chars=%s] [trimmed_chars=%s]",
            len(context),
            len(trimmed),
        )
        return trimmed

    def _build_extractive_fallback(self, query: str, documents: List[Dict[str, Any]]) -> str:
        """Build a grounded fallback answer directly from retrieved text."""
        if not documents:
            return (
                "I could not find enough policy content to answer this clearly. "
                "Please contact HR or IT for clarification."
            )

        query_terms = set(self._tokenize(query))
        if not query_terms:
            query_terms = set(re.findall(r"[a-zA-Z0-9]+", (query or "").lower()))

        selected_docs = self._select_fallback_documents(documents)
        required_overlap = 2 if len(query_terms) >= 5 else 1
        candidates = self._collect_fallback_candidates(
            selected_docs,
            query_terms,
            min_overlap=required_overlap,
        )
        if not candidates and required_overlap > 1:
            candidates = self._collect_fallback_candidates(
                selected_docs,
                query_terms,
                min_overlap=1,
            )

        if not candidates:
            top = selected_docs[0]
            source = self._format_source_ref(top.get("document", "unknown"), top.get("page"))
            preview = re.sub(r"\s+", " ", top.get("content", "")).strip()[:220]
            return (
                "I could not generate a full response in time. "
                f"Most relevant policy text found: {preview}. "
                f"Source: {source}."
            )

        candidates.sort(key=lambda x: x[0], reverse=True)

        selected = []
        seen = set()
        for _, segment, doc_name, page in candidates:
            dedup_key = segment.lower()
            if dedup_key in seen:
                continue
            seen.add(dedup_key)
            selected.append((segment, doc_name, page))
            if len(selected) >= settings.AGENT_FALLBACK_MAX_POINTS:
                break

        covered_terms = set()
        for segment, _, _ in selected:
            covered_terms.update(self._tokenize(segment))
        query_display_terms = self._build_query_display_terms(query)
        missing_terms = []
        for term in query_terms:
            if term in covered_terms:
                continue
            display = query_display_terms.get(term)
            if not display:
                continue
            if display not in missing_terms:
                missing_terms.append(display)
            if len(missing_terms) >= 3:
                break

        lines = [
            "I could not finish full model generation within the response-time target, "
            "so here are the most relevant policy points found directly in documents:"
        ]

        if missing_terms:
            lines.append(
                "Some parts of your question are not explicitly available in the retrieved text: "
                + ", ".join(missing_terms)
                + "."
            )

        for idx, (segment, doc_name, page) in enumerate(selected, 1):
            source = self._format_source_ref(doc_name, page)
            lines.append(f"{idx}. {segment} (source: {source})")

        return "\n".join(lines)

    @staticmethod
    def _build_direct_fallback(query: str) -> str:
        """Fallback answer when direct mode cannot call LLM in time."""
        lowered = (query or "").lower()
        if any(term in lowered for term in ("hello", "hi", "hey", "thanks", "thank you")):
            return (
                "I am having a temporary model-capacity issue right now, "
                "but I am here. Please try again in a few seconds."
            )
        return (
            "I could not complete the direct model response within the response-time target. "
            "Please retry in a few seconds."
        )

    @staticmethod
    def _select_fallback_documents(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Keep only top-relevance docs for fallback to avoid cross-policy noise."""
        if not documents:
            return []

        sorted_docs = sorted(
            documents,
            key=lambda d: float(d.get("relevance_score") or 0.0),
            reverse=True,
        )
        best = float(sorted_docs[0].get("relevance_score") or 0.0)
        kept = []
        for doc in sorted_docs:
            score = float(doc.get("relevance_score") or 0.0)
            if best > 0 and score < (best - FALLBACK_DOC_SCORE_MARGIN):
                continue
            kept.append(doc)
            if len(kept) >= FALLBACK_MAX_DOCS:
                break

        return kept or [sorted_docs[0]]

    @staticmethod
    def _collect_fallback_candidates(
        docs: List[Dict[str, Any]],
        query_terms: set,
        min_overlap: int,
    ) -> List[tuple]:
        """Collect scored extractive segments from selected documents."""
        candidates: List[tuple] = []

        for doc in docs:
            doc_name = doc.get("document", "unknown")
            page = doc.get("page")
            doc_score = float(doc.get("relevance_score") or 0.0)

            for segment in AIAgent._split_segments(doc.get("content", "")):
                cleaned = re.sub(r"\s+", " ", segment).strip()
                cleaned = re.sub(r"^---\s*Page\s*\d+\s*---\s*", "", cleaned, flags=re.IGNORECASE)
                if len(cleaned) < 16:
                    continue

                seg_terms = set(AIAgent._tokenize(cleaned))
                overlap = len(query_terms.intersection(seg_terms))
                if overlap < min_overlap:
                    continue

                score = (1.5 * float(overlap)) + (2.0 * doc_score)
                if any(ch.isdigit() for ch in cleaned):
                    score += 0.1

                length_penalty = min(len(cleaned) / 600.0, 0.4)
                score -= length_penalty
                candidates.append((score, cleaned, doc_name, page))

        return candidates

    @staticmethod
    def _split_segments(text: str) -> List[str]:
        """Split raw content into sentence/line-like segments for extractive fallback."""
        if not text:
            return []

        normalized = text.replace("\r\n", "\n").replace("\r", "\n")
        paragraphs = [p.strip() for p in re.split(r"\n{2,}", normalized) if p and p.strip()]

        segments: List[str] = []
        for paragraph in paragraphs:
            joined = re.sub(r"\n+", " ", paragraph).strip()
            if not joined:
                continue
            parts = [
                part.strip()
                for part in re.split(r"(?<=[.!?])\s+", joined)
                if part and part.strip()
            ]
            segments.extend(parts if parts else [joined])

        return segments

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """Tokenize to simple alphanumeric terms and remove tiny/common words."""
        stopwords = {
            "the", "and", "for", "with", "that", "this", "from", "are", "was", "were",
            "you", "your", "our", "but", "not", "can", "what", "when", "how", "who",
            "into", "onto", "over", "under", "than", "then", "have", "has", "had",
            "policy", "policies", "guideline", "guidelines", "employee", "employees",
            "company", "weeks",
        }
        raw_terms = re.findall(r"[a-zA-Z0-9]+", (text or "").lower())
        terms = [AIAgent._normalize_term(t) for t in raw_terms]
        return [t for t in terms if len(t) > 2 and t not in stopwords]

    @staticmethod
    def _normalize_term(term: str) -> str:
        """Apply lightweight normalization to improve token overlap matching."""
        t = term.lower().strip()
        for suffix in ("ingly", "edly", "ing", "ed", "es", "s"):
            if len(t) > 5 and t.endswith(suffix):
                t = t[: -len(suffix)]
                break
        return t

    @staticmethod
    def _build_query_display_terms(query: str) -> Dict[str, str]:
        """Map normalized query terms back to readable surface forms."""
        display_map: Dict[str, str] = {}
        for raw in re.findall(r"[a-zA-Z0-9]+", (query or "").lower()):
            norm = AIAgent._normalize_term(raw)
            if len(norm) <= 2:
                continue
            if norm not in display_map:
                display_map[norm] = raw
        return display_map

    @staticmethod
    def _format_source_ref(document: str, page: Optional[int]) -> str:
        """Format a plain-text source reference."""
        if page:
            return f"{document}, page {page}"
        return document

    def _format_chat_history(
        self,
        history: List[Dict[str, str]]
    ) -> List[Any]:
        """
        Format conversation history for LangChain.

        Args:
            history: List of message dicts with role and content

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


# Global agent instance
agent = AIAgent()