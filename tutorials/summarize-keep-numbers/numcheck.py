import re
import sys
from pathlib import Path

# A number is digits with optional comma groups and decimals. A letter or dot
# right before it (as in Q3 or v2.1) means it is part of a name, so it is skipped.
NUMBER = re.compile(r"(?<![\w.])\d[\d,]*(?:\.\d+)?")


def extract_numbers(text):
    """Return the set of numbers in text, with commas removed: '1,284,500' -> '1284500'."""
    found = set()
    for match in NUMBER.findall(text):
        value = match.rstrip(",").replace(",", "")
        if "." in value:
            value = value.rstrip("0").rstrip(".")  # 7.0 and 7 are the same number
        found.add(value)
    return found


def compare(source, summary):
    """Return (kept, missing, not_in_source) as sorted lists of number strings."""
    src, out = extract_numbers(source), extract_numbers(summary)
    order = lambda values: sorted(values, key=float)
    return order(src & out), order(src - out), order(out - src)


def report(source, summary):
    kept, missing, extra = compare(source, summary)
    total = len(kept) + len(missing)
    print(f"Source numbers: {total}")
    print(f"Kept in summary: {len(kept)}")
    print(f"Missing from summary: {len(missing)}")
    if missing:
        print("  " + ", ".join(missing))
    print(f"In summary but not in source: {len(extra)}")
    if extra:
        print("  " + ", ".join(extra))


def read(path):
    file = Path(path)
    if not file.is_file():
        sys.exit(f"Cannot find {path}")
    return file.read_text(encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        values = sorted(extract_numbers(read(sys.argv[1])), key=float)
        print(f"{len(values)} distinct numbers in {sys.argv[1]}")
        print(", ".join(values))
    elif len(sys.argv) == 3:
        report(read(sys.argv[1]), read(sys.argv[2]))
    else:
        sys.exit("Usage: python numcheck.py SOURCE [SUMMARY]")
