"""Decision router to determine if query needs RAG or can be answered directly."""

import re
from typing import Tuple
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class DecisionRouter:
    """Routes queries to appropriate handling strategy (direct answer vs RAG)."""

    # Keywords that indicate policy/document queries
    POLICY_KEYWORDS = {
        "policy", "policies", "leave", "vacation", "sick", "parental",
        "expense", "expenses", "travel", "reimbursement", "claim",
        "remote", "work from home", "wfh", "hybrid",
        "security", "password", "vpn", "data", "confidential",
        "hr", "human resources", "onboarding", "performance",
        "benefit", "benefits", "insurance", "401k", "pension",
        "salary", "compensation", "bonus", "raise",
        "offboarding", "resignation", "termination", "notice period",
        "holiday", "holidays", "public holiday", "time off",
        "equipment", "laptop", "monitor", "stipend",
        "guideline", "guidelines", "procedure", "procedures",
        "rule", "rules", "regulation", "regulations",
        "handbook", "manual", "document", "documentation",
        "how many days", "how much", "what is the policy",
        "can i", "am i allowed", "am i eligible",
        "approval", "approve", "manager approval"
    }

    # Domain terms that should strongly bias routing toward policy RAG.
    EXPENSE_POLICY_TERMS = {
        "expense", "expenses", "reimbursement", "reimburse", "claim", "receipt", "receipts",
        "mileage", "per diem", "hotel", "lodging", "flight", "airfare", "travel",
        "taxi", "uber", "lyft", "meal", "meals", "dinner", "alcohol",
        "approval", "approver", "approves", "manager", "cfo", "pre-approval",
        "submit", "submission", "timeline", "deadline", "business days", "limit", "max",
        "airbnb", "corporate housing", "$", "usd",
    }

    # Question markers to identify policy intent when combined with domain terms.
    QUESTION_INTENT_MARKERS = {
        "what", "when", "who", "how", "can i", "do i", "should i", "is it",
        "allowed", "eligible", "approve", "approval", "rate", "amount", "above", "below",
    }

    # Greetings and general queries that don't need RAG
    GENERAL_PATTERNS = [
        r"^(hi|hello|hey|greetings|good morning|good afternoon|good evening)",
        r"(how are you|what's up|how do you do)",
        r"(thank you|thanks|appreciate)",
        r"(bye|goodbye|see you|farewell)",
        r"(what can you do|help me|what are you)",
        r"(who are you|what is your name)",
    ]

    # Question words that often indicate policy queries
    QUESTION_WORDS = {"what", "how", "when", "where", "why", "can", "may", "should"}

    def __init__(self, confidence_threshold: float = 0.6):
        """
        Initialize decision router.

        Args:
            confidence_threshold: Minimum confidence to use RAG (0-1)
        """
        self.confidence_threshold = confidence_threshold
        logger.info(f"DecisionRouter initialized with threshold={confidence_threshold}")

    def decide(self, query: str) -> Tuple[str, float]:
        """
        Decide whether to use RAG or direct answer.

        Args:
            query: User query string

        Returns:
            Tuple of (decision, confidence) where decision is "rag_search" or "direct_answer"
        """
        normalized = (query or "").strip().lower()

        if not normalized:
            logger.info("Decision: direct_answer (empty query)")
            return "direct_answer", 0.0

        if settings.AGENT_FORCE_RAG_MODE:
            logger.info("Decision: rag_search (forced RAG mode enabled)")
            return "rag_search", 1.0

        if self._is_general_query(normalized):
            logger.info("Decision: direct_answer (general conversation)")
            return "direct_answer", 0.9

        policy_score = self._calculate_policy_score(normalized)
        is_policy_question = self._is_policy_question(normalized)
        expense_policy_intent = self._is_expense_policy_intent(normalized)

        explicit_doc_intent = any(
            marker in normalized
            for marker in (
                "according to",
                "from the policy",
                "from policy",
                "from the handbook",
                "in the handbook",
                "policy document",
                "company policy",
            )
        )

        use_rag = (
            policy_score >= self.confidence_threshold
            or (is_policy_question and policy_score >= 0.25)
            or explicit_doc_intent
            or expense_policy_intent
        )

        if use_rag:
            min_confidence = 0.75 if expense_policy_intent else (0.65 if is_policy_question else 0.5)
            confidence = min(1.0, max(policy_score, min_confidence))
            logger.info(
                "Decision: rag_search (score=%.2f, policy_q=%s, explicit_doc=%s, expense_intent=%s)",
                policy_score,
                is_policy_question,
                explicit_doc_intent,
                expense_policy_intent,
            )
            return "rag_search", confidence

        confidence = max(0.0, min(1.0, 1.0 - policy_score))
        logger.info(
            "Decision: direct_answer (score=%.2f, policy_q=%s, expense_intent=%s)",
            policy_score,
            is_policy_question,
            expense_policy_intent,
        )
        return "direct_answer", confidence

    def _is_general_query(self, query: str) -> bool:
        """Check if query is a general greeting or small talk."""
        for pattern in self.GENERAL_PATTERNS:
            if re.search(pattern, query, re.IGNORECASE):
                return True
        return False

    def _calculate_policy_score(self, query: str) -> float:
        """
        Calculate how likely the query is about company policies.

        Returns a score between 0 and 1.
        """
        words = set(query.split())
        matches = 0
        total_keywords = len(self.POLICY_KEYWORDS)

        # Check for keyword matches
        for keyword in self.POLICY_KEYWORDS:
            if keyword in query:
                # Multi-word keywords get higher weight
                weight = len(keyword.split())
                matches += weight

        # Normalize score
        if total_keywords == 0:
            return 0.0

        score = min(matches / 5.0, 1.0)  # Cap at 1.0, normalize by 5 matches
        return score

    def _is_expense_policy_intent(self, query: str) -> bool:
        """Detect expense-policy queries that should almost always go through RAG."""
        has_domain_term = any(term in query for term in self.EXPENSE_POLICY_TERMS)
        if not has_domain_term:
            return False

        # Domain + interrogative/constraint marker is a strong policy signal.
        has_question_marker = (
            "?" in query
            or any(marker in query for marker in self.QUESTION_INTENT_MARKERS)
        )
        return has_question_marker

    def _is_policy_question(self, query: str) -> bool:
        """
        Check if query is asking a question about policies.

        Looks for question words combined with business/policy context.
        """
        words = query.split()

        if not words:
            return False

        # Check if first word is a question word
        first_word = words[0].rstrip("?")
        if first_word not in self.QUESTION_WORDS:
            return False

        # Check if query contains business/corporate context
        business_terms = {
            "company", "corporate", "organization", "employee", "staff",
            "office", "work", "job", "business", "department", "team"
        }

        return any(term in query for term in business_terms)


# Global router instance
decision_router = DecisionRouter()
