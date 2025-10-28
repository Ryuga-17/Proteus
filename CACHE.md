# HTTP Caching

This adds a lightweight, optional on-disk cache for HTTP GET requests that respects origin cache validators.

## What it does
- On first request (status 200), stores response body and headers on disk keyed by URL and selected request headers.
- On subsequent requests, performs a conditional GET using `If-None-Match` and/or `If-Modified-Since` derived from the cached `ETag`/`Last-Modified` headers.
- If the server replies `304 Not Modified`, the cached body is returned, skipping re-download.
- Supports bypassing the cache with a `--no-cache` flag.

## CLI Usage
```bash
python bin/fetch_cli.py https://example.com --show-headers
python bin/fetch_cli.py https://example.com --no-cache
python bin/fetch_cli.py https://example.com --cache-dir /tmp/mycache
```

- `--no-cache`: disable cache read/write and conditional requests
- `--cache-dir`: directory for cache files; defaults to `~/.sales_agent_cache`

## Cache Location and Format
- Default directory: `~/.sales_agent_cache`
- Files per entry:
  - `<key>.meta.json`: URL, status_code, response headers, created timestamp
  - `<key>.body`: raw response bytes
- Cache key: SHA-256 of `URL` plus any configured vary request headers (default: `Accept`).

## Integration API
Use `cached_get` from `cache/fetch.py`:
```python
from cache.fetch import cached_get

status, headers, body, from_cache = cached_get(
    "https://example.com/data.json",
    headers={"Accept": "application/json"},
    cache_dir="~/.sales_agent_cache",
    no_cache=False,
)
```

Returns `(status_code, response_headers, body_bytes, from_cache: bool)`.

## Acceptance Criteria
- Repeated runs against the same URL with unchanged content avoid re-downloading and return results faster via `304` validation and on-disk cache.

## Notes
- Currently caches successful `200` responses. Other codes are returned but not cached.
- Honors `ETag` and `Last-Modified` if provided by the origin server; falls back to network when absent.
- Extend `vary_headers` in `cached_get` if specific request headers should participate in the cache key.


