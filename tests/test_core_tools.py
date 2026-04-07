from app.agent.core import AIAgent


class _DummyLLM:
    async def ainvoke(self, _messages):
        class _Response:
            content = "ok"

        return _Response()


def _build_agent(monkeypatch):
    monkeypatch.setattr(AIAgent, "_initialize_llm", lambda self: _DummyLLM())
    return AIAgent()


def test_detects_calculator_tool(monkeypatch):
    agent = _build_agent(monkeypatch)
    tool_call = agent._detect_tool_call("calculate 12 * (5 + 3)")
    assert tool_call is not None
    assert tool_call["name"] == "calculator"


def test_executes_calculator_tool(monkeypatch):
    agent = _build_agent(monkeypatch)
    result = agent._execute_tool_call({"name": "calculator", "input": "2 + 3"})
    assert result["answer"] == "2 + 3 = 5"
    assert result["sources"] == []


def test_response_contract_appends_sources(monkeypatch):
    agent = _build_agent(monkeypatch)
    output = agent._apply_response_contract(
        answer="The CFO approves this level.",
        decision="rag_search",
        sources=[{"document": "expense_policy.pdf", "page": 3}],
        fallback_used=False,
        fallback_reason=None,
    )
    assert "Sources:" in output
    assert "expense_policy.pdf" in output
