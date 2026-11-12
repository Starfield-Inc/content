"""Pull action items out of meeting notes. Plain rules, no model, no network."""
import re
import sys
from pathlib import Path

MARKERS = re.compile(r"^\s*-?\s*(todo|action)\s*:\s*(.+)$", re.I)
WILL = re.compile(r"^\s*-\s*(\w+) will (.+)$", re.I)


def action_items(text):
    items = []
    for line in text.splitlines():
        if m := MARKERS.match(line):
            items.append(m.group(2).strip())
        elif m := WILL.match(line):
            items.append(f"{m.group(1)}: {m.group(2).strip().rstrip('.')}")
    return items


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python app.py notes.txt")
    path = Path(sys.argv[1])
    if not path.is_file():
        sys.exit(f"Cannot find {path}")
    items = action_items(path.read_text(encoding="utf-8"))
    print(f"Found {len(items)} action items in {path.name}")
    for n, item in enumerate(items, 1):
        print(f"  {n}. {item}")


if __name__ == "__main__":
    main()
