"""
Session Manager
Maintains per-user conversation state using Redis (or in-memory dict as fallback).
Sessions expire after 30 minutes of inactivity.
"""

import os
import json
import time
from typing import Optional

try:
    import redis
    _redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    _redis_client = redis.from_url(_redis_url, decode_responses=True)
    _redis_client.ping()
    USE_REDIS = True
    print("[SessionManager] Using Redis for session storage.")
except Exception as e:
    USE_REDIS = False
    _in_memory_store: dict = {}
    print(f"[SessionManager] Redis unavailable ({e}). Using in-memory store.")

SESSION_TTL = 1800  # 30 minutes


def _key(phone: str) -> str:
    return f"namma_market:session:{phone}"


def get_session(phone: str) -> dict:
    """Retrieve session for a user. Returns empty dict if not found."""
    try:
        if USE_REDIS:
            raw = _redis_client.get(_key(phone))
            if raw:
                _redis_client.expire(_key(phone), SESSION_TTL)
                return json.loads(raw)
        else:
            entry = _in_memory_store.get(phone)
            if entry and (time.time() - entry["_ts"] < SESSION_TTL):
                return entry["data"]
    except Exception as e:
        print(f"[SessionManager] get_session error: {e}")
    return {}


def save_session(phone: str, session: dict) -> None:
    """Save session for a user."""
    try:
        if USE_REDIS:
            _redis_client.setex(_key(phone), SESSION_TTL, json.dumps(session))
        else:
            _in_memory_store[phone] = {"data": session, "_ts": time.time()}
    except Exception as e:
        print(f"[SessionManager] save_session error: {e}")


def clear_session(phone: str) -> None:
    """Clear session for a user."""
    try:
        if USE_REDIS:
            _redis_client.delete(_key(phone))
        else:
            _in_memory_store.pop(phone, None)
    except Exception as e:
        print(f"[SessionManager] clear_session error: {e}")


def update_session(phone: str, updates: dict) -> dict:
    """Merge updates into existing session and save."""
    session = get_session(phone)
    session.update(updates)
    save_session(phone, session)
    return session
