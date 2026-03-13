#!/usr/bin/env python3
"""
Save a spark note to Notion's Daily Spark Notes page.
Organizes entries under date headings (H2). Appends to today's section or creates one.

Usage:
    python save_to_notion.py --type text --content "Your note here"
    python save_to_notion.py --type url --content "https://example.com" --title "Page Title" --summary "Brief summary"

Env:
    NOTION_API_KEY  - Notion integration token (required)

The target page ID is hardcoded from:
https://www.notion.so/Daily-Spark-Notes-3197a36253538014aeb7ef4d59fc7349
"""

import argparse
import json
import os
import sys
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import HTTPError

PAGE_ID = "3197a362-5353-8014-aeb7-ef4d59fc7349"
NOTION_VERSION = "2022-06-28"


def get_api_key():
    key = os.environ.get("NOTION_API_KEY")
    if not key:
        print("Error: NOTION_API_KEY environment variable is required.", file=sys.stderr)
        sys.exit(1)
    return key


def notion_request(method, endpoint, body=None):
    api_key = get_api_key()
    url = f"https://api.notion.com/v1{endpoint}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode() if body else None
    req = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read())
    except HTTPError as e:
        error_body = e.read().decode()
        print(f"Notion API error ({e.code}): {error_body}", file=sys.stderr)
        sys.exit(1)


def get_all_children(block_id):
    """Retrieve all child blocks of a page/block, handling pagination."""
    children = []
    cursor = None
    while True:
        endpoint = f"/blocks/{block_id}/children?page_size=100"
        if cursor:
            endpoint += f"&start_cursor={cursor}"
        result = notion_request("GET", endpoint)
        children.extend(result.get("results", []))
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")
    return children


def find_today_heading(block_id):
    """Find the H2 heading block for today's date. Returns block_id or None."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    children = get_all_children(block_id)
    for block in children:
        if block.get("type") == "heading_2":
            rich_text = block["heading_2"].get("rich_text", [])
            text = "".join(rt.get("plain_text", "") for rt in rich_text)
            if text.strip() == today_str:
                return block["id"]
    return None


def make_rich_text(content, bold=False, link=None):
    rt = {"type": "text", "text": {"content": content}}
    if link:
        rt["text"]["link"] = {"url": link}
    if bold:
        rt["annotations"] = {"bold": True}
    return rt


def build_text_blocks(content):
    """Build blocks for a plain text note."""
    now = datetime.now().strftime("%H:%M")
    return [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    make_rich_text(f"[{now}] ", bold=True),
                    make_rich_text(content),
                ]
            },
        }
    ]


def build_url_blocks(url, title, summary):
    """Build blocks for a URL note: bookmark + summary paragraph."""
    now = datetime.now().strftime("%H:%M")
    blocks = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    make_rich_text(f"[{now}] ", bold=True),
                    make_rich_text(title or url, link=url),
                ]
            },
        },
    ]
    if summary:
        blocks.append(
            {
                "object": "block",
                "type": "quote",
                "quote": {
                    "rich_text": [make_rich_text(summary)]
                },
            }
        )
    blocks.append(
        {
            "object": "block",
            "type": "bookmark",
            "bookmark": {"url": url},
        }
    )
    return blocks


def create_today_heading_and_append(page_id, content_blocks):
    """Create today's H2 heading, then append content blocks under it."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    # Append heading + divider + content in one call
    blocks = [
        {
            "object": "block",
            "type": "divider",
            "divider": {},
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [make_rich_text(today_str)],
            },
        },
    ] + content_blocks
    notion_request("PATCH", f"/blocks/{page_id}/children", {"children": blocks})


def append_after_heading(page_id, heading_block_id, content_blocks):
    """Append content blocks after the existing today heading."""
    # Find all children to locate the last block under today's heading
    children = get_all_children(page_id)
    # Find the index of the heading
    heading_idx = None
    for i, block in enumerate(children):
        if block["id"] == heading_block_id:
            heading_idx = i
            break
    if heading_idx is None:
        # Fallback: just append
        notion_request("PATCH", f"/blocks/{page_id}/children", {"children": content_blocks})
        return

    # Find the last block that belongs to today's section
    # (everything between this H2 and the next H2 or divider-before-H2, or end)
    last_block_id = heading_block_id
    for j in range(heading_idx + 1, len(children)):
        block = children[j]
        if block.get("type") in ("heading_2", "divider"):
            break
        last_block_id = block["id"]

    notion_request(
        "PATCH",
        f"/blocks/{page_id}/children",
        {"children": content_blocks, "after": last_block_id},
    )


def main():
    parser = argparse.ArgumentParser(description="Save a spark note to Notion")
    parser.add_argument("--type", required=True, choices=["text", "url"], help="Note type")
    parser.add_argument("--content", required=True, help="Note content or URL")
    parser.add_argument("--title", default="", help="URL page title (for url type)")
    parser.add_argument("--summary", default="", help="URL page summary (for url type)")
    args = parser.parse_args()

    if args.type == "text":
        blocks = build_text_blocks(args.content)
    else:
        blocks = build_url_blocks(args.content, args.title, args.summary)

    heading_id = find_today_heading(PAGE_ID)
    if heading_id:
        append_after_heading(PAGE_ID, heading_id, blocks)
    else:
        create_today_heading_and_append(PAGE_ID, blocks)

    print(f"Saved to Notion (Daily Spark Notes, {datetime.now().strftime('%Y-%m-%d %H:%M')})")


if __name__ == "__main__":
    main()
