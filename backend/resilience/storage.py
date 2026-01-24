import json
import os
import threading
from datetime import datetime
from typing import Any, Callable, Dict


def utc_now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


class FileBackedStore:
    """
    Minimal JSON file store with atomic writes and a process-local lock.
    Designed for demo resilience, not multi-process safety.
    """

    def __init__(self, path: str, default_factory: Callable[[], Dict[str, Any]]):
        self.path = path
        self.default_factory = default_factory
        self.lock = threading.Lock()
        self._ensure_file()

    def _ensure_file(self) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            self._write(self.default_factory())

    def _read(self) -> Dict[str, Any]:
        try:
            with open(self.path, "r") as handle:
                return json.load(handle)
        except Exception:
            return self.default_factory()

    def _write(self, data: Dict[str, Any]) -> None:
        temp_path = f"{self.path}.tmp"
        with open(temp_path, "w") as handle:
            json.dump(data, handle, indent=2, sort_keys=True)
        os.replace(temp_path, self.path)

    def get(self) -> Dict[str, Any]:
        with self.lock:
            return self._read()

    def update(self, updater: Callable[[Dict[str, Any]], Dict[str, Any]]) -> Dict[str, Any]:
        with self.lock:
            data = self._read()
            updated = updater(data)
            self._write(updated)
            return updated
