import json
import sys
from pathlib import Path

import feedparser

MAX_PER_FEED = 25


def main() -> int:
    urls = [u.strip() for u in Path("feeds.txt").read_text().splitlines() if u.strip()]
    items = []
    for url in urls:
        feed = feedparser.parse(url, agent="labs-tutorial-news-dedupe/1.0")
        if feed.bozo and not feed.entries:
            print(f"skipped {url}: could not read the feed", file=sys.stderr)
            continue
        source = feed.feed.get("title", url)
        for entry in feed.entries[:MAX_PER_FEED]:
            items.append({"source": source, "title": entry.get("title", "").strip(),
                          "link": entry.get("link", ""), "published": entry.get("published", "")})
        print(f"{source}: {min(len(feed.entries), MAX_PER_FEED)} items")
    Path("items.json").write_text(json.dumps(items, indent=2), encoding="utf-8")
    print(f"Saved {len(items)} items to items.json")
    return 0 if items else 1


if __name__ == "__main__":
    sys.exit(main())
