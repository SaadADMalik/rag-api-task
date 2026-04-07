"""Decision router to determine if query needs RAG or can be answered directly."""

import re
from typing import Tuple
import logging

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
        _ = query  # Query is intentionally unused when RAG is mandatory.
        logger.info("Decision: rag_search (forced RAG mode enabled)")
        return "rag_search", 1.0

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
