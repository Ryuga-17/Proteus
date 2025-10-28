import os
from typing import Dict, Optional, Tuple

import requests

from .http_cache import HTTPCache


def _extract_conditionals(resp_headers: Dict[str, str]) -> Dict[str, str]:
    etag = resp_headers.get("ETag") or resp_headers.get("etag")
    last_modified = resp_headers.get("Last-Modified") or resp_headers.get("last-modified")
    out: Dict[str, str] = {}
    if etag:
        out["If-None-Match"] = etag
    if last_modified:
        out["If-Modified-Since"] = last_modified
    return out


def cached_get(
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    timeout: float = 30.0,
    cache_dir: Optional[str] = None,
    no_cache: bool = False,
    vary_headers: Tuple[str, ...] = ("accept",),
) -> Tuple[int, Dict[str, str], bytes, bool]:
    """
    Perform an HTTP GET with on-disk caching and conditional requests.

    Returns (status_code, response_headers, body_bytes, from_cache)
    """
    headers = dict(headers or {})
    cache_dir = cache_dir or os.path.join(os.path.expanduser("~"), ".sales_agent_cache")
    cache = HTTPCache(cache_dir=cache_dir, vary_headers=vary_headers)

    cached = None if no_cache else cache.read(url, headers)
    if cached:
        # Try a conditional GET to validate
        cond = _extract_conditionals(cached.headers)
        req_headers = dict(headers)
        req_headers.update(cond)
        r = requests.get(url, headers=req_headers, timeout=timeout)
        if r.status_code == 304:
            with open(cached.body_path, "rb") as f:
                body = f.read()
            return cached.status_code, cached.headers, body, True
        else:
            # Replace cache with new content
            cache.write(url, r.status_code, r.headers, r.content, headers)
            return r.status_code, dict(r.headers), r.content, False

    # No cache or bypass requested
    r = requests.get(url, headers=headers, timeout=timeout)
    if not no_cache and r.status_code == 200:
        cache.write(url, r.status_code, r.headers, r.content, headers)
    return r.status_code, dict(r.headers), r.content, False


