"""Count right and wrong for one or more results files, and list the wrong ones.

  python score.py results_v1.csv [results_v2.csv]
With two files it also lists the reviews whose prediction changed.
"""
import csv, sys
from collections import Counter

from prompts import LABELS


def load(path):
    return {r["id"]: r for r in csv.DictReader(open(path, newline=""))}


def report(path, rows):
    right = sum(r["predicted"] == r["label"] for r in rows.values())
    print(f"== {path}")
    print(f"Right: {right} of {len(rows)}")
    print(f"Wrong: {len(rows) - right}")
    for label in LABELS:
        mine = [r for r in rows.values() if r["label"] == label]
        ok = sum(r["predicted"] == label for r in mine)
        print(f"  {label}: {ok} of {len(mine)} right")
    wrong = [r for r in rows.values() if r["predicted"] != r["label"]]
    for r in wrong:
        print(f"  #{r['id']} wrote {r['label']}, model said {r['raw']!r}: {r['text'][:72]}")
    return right


def main():
    paths = sys.argv[1:]
    runs = [load(p) for p in paths]
    for p, rows in zip(paths, runs):
        report(p, rows)
    if len(runs) == 2:
        a, b = runs
        changed = [i for i in a if a[i]["predicted"] != b[i]["predicted"]]
        print(f"== Changed between runs: {len(changed)}")
        for i in changed:
            ok_a, ok_b = a[i]["predicted"] == a[i]["label"], b[i]["predicted"] == b[i]["label"]
            print(f"  #{i} {a[i]['predicted']} -> {b[i]['predicted']} (label {a[i]['label']}, "
                  f"{'right' if ok_a else 'wrong'} -> {'right' if ok_b else 'wrong'})")


if __name__ == "__main__":
    main()
