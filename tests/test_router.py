from app.agent.router import DecisionRouter
from app.config import settings


def test_greeting_routes_direct_answer():
    router = DecisionRouter()
    decision, confidence = router.decide("hello there")
    assert decision == "direct_answer"
    assert confidence >= 0.5


def test_expense_query_routes_to_rag():
    router = DecisionRouter()
    decision, confidence = router.decide("What is the mileage reimbursement rate?")
    assert decision == "rag_search"
    assert confidence >= 0.5


def test_force_rag_mode_overrides_routing(monkeypatch):
    monkeypatch.setattr(settings, "AGENT_FORCE_RAG_MODE", True)
    router = DecisionRouter()
    decision, confidence = router.decide("hello")
    assert decision == "rag_search"
    assert confidence == 1.0
