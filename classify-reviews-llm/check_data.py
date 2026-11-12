"""Check reviews.csv: count the rows and the labels."""
import csv
from collections import Counter

from prompts import LABELS

rows = list(csv.DictReader(open("reviews.csv", newline="")))
counts = Counter(r["label"] for r in rows)
bad = [r["id"] for r in rows if r["label"] not in LABELS]
print(f"Reviews: {len(rows)}")
for label in LABELS:
    print(f"  {label}: {counts[label]}")
print(f"Rows with an unknown label: {len(bad)}")
for r in rows[:3]:
    print(f"  {r['id']} [{r['label']}] {r['text']}")
