import json

from prompts import LABELS


def read_label(raw):
    """The opening word of the reply, upper case. Anything that is not a label counts as wrong."""
    words = raw.strip().upper().split()
    word = words[0].strip(".,:*") if words else ""
    return word if word in LABELS else None


def score(mode):
    results = json.load(open(f"results_{mode}.json"))
    failures = [r for r in results if read_label(r["raw"]) != r["expected"]]
    return len(results) - len(failures), len(results), failures


for mode in ("zero", "few"):
    right, total, failures = score(mode)
    print(f"{mode}-shot: {right} of {total} correct")
    for r in failures:
        print(f"  #{r['id']} expected {r['expected']}, got {r['raw'].strip()!r}: {r['text']}")
