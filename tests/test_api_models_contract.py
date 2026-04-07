import pytest
from pydantic import ValidationError

from app.models import AskRequest


def test_ask_request_accepts_valid_payload():
    req = AskRequest(query="hello", session_id="session-abc_123")
    assert req.query == "hello"
    assert req.session_id == "session-abc_123"


def test_ask_request_rejects_invalid_session_id():
    with pytest.raises(ValidationError):
        AskRequest(query="hello", session_id="bad id with spaces")


def test_ask_request_rejects_extra_fields():
    with pytest.raises(ValidationError):
        AskRequest(query="hello", session_id="session-ok", unknown_field="x")
