import json
from typing import Any, Dict, Optional
from .storage import utc_now_iso


def log_event(event: str, level: str = "info", details: Optional[Dict[str, Any]] = None) -> None:
    payload = {
        "ts": utc_now_iso(),
        "event": event,
        "level": level,
        "details": details or {},
    }
    print(json.dumps(payload, sort_keys=True))
