from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict
from .storage import utc_now_iso


@dataclass
class CircuitBreakerState:
    state: str
    failure_count: int
    opened_at: str


class CircuitBreaker:
    def __init__(self, name: str, store):
        self.name = name
        self.store = store

    def _load_state(self) -> CircuitBreakerState:
        data = self.store.get()
        record = data.get(self.name, {})
        return CircuitBreakerState(
            state=record.get("state", "closed"),
            failure_count=record.get("failure_count", 0),
            opened_at=record.get("opened_at", ""),
        )

    def allow_request(self, max_failures: int, open_duration_seconds: int) -> bool:
        state = self._load_state()
        if state.state != "open":
            return True
        if not state.opened_at:
            return False
        opened_dt = datetime.fromisoformat(state.opened_at.replace("Z", "+00:00"))
        if datetime.utcnow().replace(tzinfo=opened_dt.tzinfo) > opened_dt + timedelta(seconds=open_duration_seconds):
            self.record_success()
            return True
        return False

    def record_success(self) -> None:
        def _update(data: Dict[str, dict]) -> Dict[str, dict]:
            data[self.name] = {
                "state": "closed",
                "failure_count": 0,
                "opened_at": "",
            }
            return data

        self.store.update(_update)

    def record_failure(self, max_failures: int) -> None:
        def _update(data: Dict[str, dict]) -> Dict[str, dict]:
            record = data.get(self.name, {"state": "closed", "failure_count": 0, "opened_at": ""})
            record["failure_count"] = record.get("failure_count", 0) + 1
            if record["failure_count"] >= max_failures:
                record["state"] = "open"
                record["opened_at"] = utc_now_iso()
            data[self.name] = record
            return data

        self.store.update(_update)
