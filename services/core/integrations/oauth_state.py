"""OAuth state store: maps a random state token to the initiating user."""
import json
import secrets
import time
from typing import Optional

from services.core.config import settings

_TTL = 600  # seconds
_memory: dict[str, tuple[float, str]] = {}  # state -> (expiry_ts, payload_json)


def _redis():
    try:
        import redis
        r = redis.Redis.from_url(settings.REDIS_URL, socket_connect_timeout=2)
        r.ping()
        return r
    except Exception:
        return None


def create_state(user_id: str, platform: str) -> str:
    state = secrets.token_urlsafe(24)
    payload = json.dumps({"user_id": user_id, "platform": platform})
    r = _redis()
    if r:
        r.setex(f"oauth_state:{state}", _TTL, payload)
    else:
        _memory[state] = (time.time() + _TTL, payload)
    return state


def pop_state(state: str) -> Optional[dict]:
    r = _redis()
    if r:
        key = f"oauth_state:{state}"
        payload = r.get(key)
        if payload:
            r.delete(key)
            return json.loads(payload)
        return None
    expiry_payload = _memory.pop(state, None)
    if expiry_payload and expiry_payload[0] > time.time():
        return json.loads(expiry_payload[1])
    return None
