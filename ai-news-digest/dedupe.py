import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit


def link_key(link: str) -> str:
    """Same page, different tracking tail: drop the query, fragment and trailing slash."""
    parts = urlsplit(link.strip().lower())
    return f"{parts.netloc.removeprefix('www.')}{parts.path.rstrip('/')}"


def title_key(title: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", title.lower()))


def dedupe(items: list[dict]) -> list[dict]:
    seen_links, seen_titles, kept = set(), set(), []
    for item in items:
        lk, tk = link_key(item["link"]), title_key(item["title"])
        if lk in seen_links or tk in seen_titles:
            continue
        seen_links.add(lk)
        seen_titles.add(tk)
        kept.append(item)
    return kept


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("infile")
    parser.add_argument("outfile")
    parser.add_argument("--quiet", action="store_true", help="print counts only, not titles")
    args = parser.parse_args()

    items = json.loads(Path(args.infile).read_text())
    kept = dedupe(items)
    Path(args.outfile).write_text(json.dumps(kept, indent=2), encoding="utf-8")
    print(f"{len(items)} items in, {len(kept)} kept, {len(items) - len(kept)} duplicates removed")
    if not args.quiet:
        kept_ids = {id(i) for i in kept}
        for item in items:
            if id(item) not in kept_ids:
                print(f"  removed: {item['title']} ({item['source']})")


if __name__ == "__main__":
    main()
