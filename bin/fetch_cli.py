#!/usr/bin/env python3
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from cache.fetch import cached_get


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch a URL with optional on-disk caching.")
    parser.add_argument("url", help="URL to fetch")
    parser.add_argument("--no-cache", action="store_true", help="Bypass on-disk cache and conditional requests")
    parser.add_argument("--cache-dir", default=os.path.join(os.path.expanduser("~"), ".sales_agent_cache"), help="Directory to store cache entries")
    parser.add_argument("--show-headers", action="store_true", help="Print response headers to stderr")
    args = parser.parse_args()

    status, headers, body, from_cache = cached_get(
        args.url,
        cache_dir=args.cache_dir,
        no_cache=args.no_cache,
    )

    if args.show_headers:
        src = "cache" if from_cache else "network"
        print(f"Status: {status} (from {src})", file=sys.stderr)
        for k, v in headers.items():
            print(f"{k}: {v}", file=sys.stderr)

    # Write body to stdout
    sys.stdout.buffer.write(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


