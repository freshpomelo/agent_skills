#!/usr/bin/env python3
"""
Fetch URL content via Jina Reader API with browser rendering support.

Usage:
    python jina_fetch.py "https://example.com"

Env:
    JINA_API_KEY - Jina AI API key (required)

Output: JSON with keys: url, title, summary, raw_content
Always uses cf-browser-rendering to handle JS-heavy pages (WeChat, SPA, etc.).
"""

import json
import os
import sys
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError

JINA_READER_BASE_URL = "https://r.jina.ai/"


def fetch_url(url: str) -> dict:
    api_key = os.environ.get("JINA_API_KEY")
    if not api_key:
        print("Error: JINA_API_KEY environment variable is required.", file=sys.stderr)
        sys.exit(1)

    # Normalize URL
    parsed = urlparse(url)
    if not parsed.scheme:
        url = f"https://{url}"
        parsed = urlparse(url)
    if not parsed.netloc:
        print(f"Error: invalid URL: {url}", file=sys.stderr)
        sys.exit(1)

    target_url = f"{JINA_READER_BASE_URL}{url}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "X-Engine": "cf-browser-rendering",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    req = Request(target_url, headers=headers, method="GET")
    try:
        with urlopen(req, timeout=30) as resp:
            body = resp.read().decode()
    except HTTPError as e:
        error_body = e.read().decode()
        print(f"Jina Reader error ({e.code}): {error_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Jina Reader error: {e}", file=sys.stderr)
        sys.exit(1)

    data = {}
    text_body = None
    try:
        data = json.loads(body)
    except ValueError:
        text_body = body

    if text_body is None:
        text_body = (
            data.get("content")
            or data.get("text")
            or data.get("data", {}).get("content")
            or ""
        )

    title = data.get("title") or data.get("data", {}).get("title")
    description = data.get("description") or data.get("data", {}).get("description")
    summary = data.get("summary") or data.get("data", {}).get("summary")

    if not title:
        title = parsed.path.strip("/") or parsed.hostname or url

    # Build summary from available parts
    summary_parts = []
    if title:
        summary_parts.append(str(title))
    if description:
        summary_parts.append(str(description))
    if not summary_parts and text_body:
        summary_parts.append(text_body[:200])
    summary = " - ".join(summary_parts).strip()

    return {
        "url": url,
        "title": title,
        "summary": summary,
        "raw_content": text_body,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python jina_fetch.py <url>", file=sys.stderr)
        sys.exit(1)

    result = fetch_url(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
