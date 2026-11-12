import csv
from collections import Counter

from prompts import EXAMPLES, LABELS

rows = list(csv.DictReader(open("inputs.csv")))
assert len(rows) == 20, len(rows)
assert all(r["expected"] in LABELS for r in rows)
assert not {t for t, _ in EXAMPLES} & {r["text"] for r in rows}, "an example is also an input"
counts = Counter(r["expected"] for r in rows)
print(f"{len(rows)} inputs:", ", ".join(f"{label} {counts[label]}" for label in LABELS))
print("none of the 3 examples is in the inputs")
