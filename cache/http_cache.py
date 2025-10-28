import hashlib
import json
import os
import time
from dataclasses import dataclass
from typing import Dict, Optional, Tuple


def _stable_key(parts: Tuple[str, ...]) -> str:
    m = hashlib.sha256()
    for p in parts:
        m.update(p.encode("utf-8"))
        m.update(b"\0")
    return m.hexdigest()


@dataclass
class CachedResponse:
    url: str
    status_code: int
    headers: Dict[str, str]
    body_path: str
    created_ts: float


class HTTPCache:
    """
    Lightweight on-disk cache keyed by URL and selected request header values.

    Stores two files per entry under cache_dir:
      - <key>.meta.json (ETag, Last-Modified, response headers, etc.)
      - <key>.body       (raw response bytes)
    """

    def __init__(self, cache_dir: str, vary_headers: Optional[Tuple[str, ...]] = None) -> None:
        self.cache_dir = cache_dir
        self.vary_headers = tuple(h.lower() for h in (vary_headers or ()))
        os.makedirs(self.cache_dir, exist_ok=True)

    def _entry_paths(self, key: str) -> Tuple[str, str]:
        meta = os.path.join(self.cache_dir, f"{key}.meta.json")
        body = os.path.join(self.cache_dir, f"{key}.body")
        return meta, body

    def _make_key(self, url: str, request_headers: Optional[Dict[str, str]]) -> str:
        request_headers = {k.lower(): v for k, v in (request_headers or {}).items()}
        vary_values = [request_headers.get(h, "") for h in self.vary_headers]
        return _stable_key((url, *vary_values))

    def read(self, url: str, request_headers: Optional[Dict[str, str]] = None) -> Optional[CachedResponse]:
        key = self._make_key(url, request_headers)
        meta_path, body_path = self._entry_paths(key)
        if not (os.path.exists(meta_path) and os.path.exists(body_path)):
            return None
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            return CachedResponse(
                url=meta["url"],
                status_code=meta["status_code"],
                headers=meta["headers"],
                body_path=body_path,
                created_ts=meta.get("created_ts", 0.0),
            )
        except Exception:
            return None

    def write(
        self,
        url: str,
        status_code: int,
        headers: Dict[str, str],
        body_bytes: bytes,
        request_headers: Optional[Dict[str, str]] = None,
    ) -> None:
        key = self._make_key(url, request_headers)
        meta_path, body_path = self._entry_paths(key)
        tmp_meta = meta_path + ".tmp"
        tmp_body = body_path + ".tmp"

        with open(tmp_body, "wb") as f:
            f.write(body_bytes)

        meta = {
            "url": url,
            "status_code": status_code,
            "headers": {k: str(v) for k, v in headers.items()},
            "created_ts": time.time(),
        }
        with open(tmp_meta, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, sort_keys=True)

        os.replace(tmp_body, body_path)
        os.replace(tmp_meta, meta_path)

    def invalidate(self, url: str, request_headers: Optional[Dict[str, str]] = None) -> None:
        key = self._make_key(url, request_headers)
        meta_path, body_path = self._entry_paths(key)
        if os.path.exists(meta_path):
            try:
                os.remove(meta_path)
            except OSError:
                pass
        if os.path.exists(body_path):
            try:
                os.remove(body_path)
            except OSError:
                pass


