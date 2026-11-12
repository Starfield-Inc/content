import argparse
import html
import json
import re
import sys
from pathlib import Path

import feedparser

AGENT = "labs-tutorial-ai-news-digest/1.0"


def plain(text: str, limit: int = 600) -> str:
    """Strip tags and extra spaces from a feed's summary and cut it to a short excerpt."""
    text = re.sub(r"<[^>]+>", " ", text or "")
    return re.sub(r"\s+", " ", html.unescape(text)).strip()[:limit]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feeds", default="feeds.txt")
    parser.add_argument("--out", default="items.json")
    parser.add_argument("--per-feed", type=int, default=3)
    args = parser.parse_args()

    urls = [u.strip() for u in Path(args.feeds).read_text().splitlines() if u.strip()]
    items = []
    for url in urls:
        feed = feedparser.parse(url, agent=AGENT)
        if feed.bozo and not feed.entries:
            print(f"skipped {url}: could not read the feed", file=sys.stderr)
            continue
        source = feed.feed.get("title", url)
        entries = feed.entries[: args.per_feed]
        for entry in entries:
            items.append({
                "source": source,
                "title": entry.get("title", "").strip(),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "text": plain(entry.get("summary", "")),
            })
        print(f"{source}: {len(entries)} items")
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(items, indent=2), encoding="utf-8")
    print(f"Saved {len(items)} items to {args.out}")
    return 0 if items else 1


if __name__ == "__main__":
    sys.exit(main())
