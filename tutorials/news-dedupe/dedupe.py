import json
import re
import sys
from pathlib import Path

STOPWORDS = {"a", "an", "and", "as", "at", "for", "from", "in", "into", "is", "it", "of", "on", "or",
             "the", "to", "with", "new", "its", "how", "what", "this", "that", "by", "your"}
THRESHOLD = 0.25


def words(title: str) -> set[str]:
    found = re.findall(r"[a-z0-9.]+", title.lower())
    return {w.strip(".") for w in found if w.strip(".") not in STOPWORDS and len(w.strip(".")) > 1}


def versions(a: set[str]) -> set[str]:
    return {w for w in a if any(ch.isdigit() for ch in w)}


def similarity(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    if versions(a) and versions(b) and not versions(a) & versions(b):
        return 0.0
    return len(a & b) / len(a | b)


def group(items: list[dict], threshold: float = THRESHOLD) -> list[list[dict]]:
    parent = list(range(len(items)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    sets = [words(item["title"]) for item in items]
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i]["source"] != items[j]["source"] and similarity(sets[i], sets[j]) >= threshold:
                parent[find(j)] = find(i)
    groups: dict[int, list[dict]] = {}
    for i, item in enumerate(items):
        groups.setdefault(find(i), []).append(item)
    return sorted(groups.values(), key=len, reverse=True)


def main() -> int:
    items = json.loads(Path("items.json").read_text())
    groups = group(items)
    repeated = [g for g in groups if len(g) > 1]
    print(f"{len(items)} items became {len(groups)} stories. {len(repeated)} stories appear in more than one feed.\n")
    for g in repeated:
        print(f"STORY ({len(g)} feeds)")
        for item in g:
            print(f"  - {item['source']}: {item['title']}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
