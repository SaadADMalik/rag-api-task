from datetime import datetime, timedelta, timezone

from app.agent.memory import SessionMemoryManager


def test_session_id_is_normalized():
    manager = SessionMemoryManager(
        max_messages_per_session=5,
        session_ttl_minutes=30,
        max_active_sessions=10,
        max_session_id_length=16,
        max_message_chars=200,
    )

    session = manager.get_or_create_session("  bad id !! with spaces  ")

    assert " " not in session.session_id
    assert "!" not in session.session_id
    assert len(session.session_id) <= 16


def test_message_cap_is_enforced():
    manager = SessionMemoryManager(
        max_messages_per_session=3,
        session_ttl_minutes=30,
        max_active_sessions=10,
        max_session_id_length=32,
        max_message_chars=200,
    )

    sid = "session-cap"
    manager.add_user_message(sid, "m1")
    manager.add_assistant_message(sid, "m2")
    manager.add_user_message(sid, "m3")
    manager.add_assistant_message(sid, "m4")

    history = manager.get_session_history(sid)
    assert len(history) == 3
    assert history[0]["content"] == "m2"


def test_expired_session_is_recreated():
    manager = SessionMemoryManager(
        max_messages_per_session=5,
        session_ttl_minutes=30,
        max_active_sessions=10,
        max_session_id_length=32,
        max_message_chars=200,
    )

    sid = "session-expire"
    manager.add_user_message(sid, "old message")
    old_session = manager.get_or_create_session(sid)
    old_session.last_accessed = datetime.now(timezone.utc) - timedelta(minutes=60)

    new_session = manager.get_or_create_session(sid)
    assert new_session.get_message_count() == 0
