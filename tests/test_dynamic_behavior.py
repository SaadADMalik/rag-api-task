from app.agent.router import DecisionRouter
from app.agent.core import AIAgent


class _DummyLLM:
    async def ainvoke(self, _messages):
        class _Response:
            content = "ok"

        return _Response()


def _build_agent(monkeypatch):
    monkeypatch.setattr(AIAgent, "_initialize_llm", lambda self: _DummyLLM())
    return AIAgent()


def test_simple_query_routes_direct():
    router = DecisionRouter()
    decision, _ = router.decide("hey there")
    assert decision == "direct_answer"


def test_complex_policy_query_routes_rag():
    router = DecisionRouter()
    decision, _ = router.decide(
        "According to expense policy, what is reimbursement submission deadline and late submission rule?"
    )
    assert decision == "rag_search"


def test_document_search_phrase_maps_to_tool_use(monkeypatch):
    agent = _build_agent(monkeypatch)
    tool_call = agent._detect_tool_call("search documents for vpn password rotation policy")
    assert tool_call is not None
    assert tool_call["name"] == "document_search"
