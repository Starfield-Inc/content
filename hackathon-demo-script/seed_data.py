"""Write the same demo data every time, so the demo never depends on live data.

Twelve made-up support tickets. Five are planned edge cases that break demos:
an empty body, a very long body, a non-English ticket, an emoji, and a duplicate.
The random generator has a fixed seed, so two runs give identical bytes.
Use --check to rebuild in memory and compare with the file on disk.
"""
import argparse
import hashlib
import json
import random
import sys
from pathlib import Path

OUT = Path("demo_data.json")
SEED = 8
CUSTOMERS = ["Ada", "Ben", "Chen", "Dara", "Eli", "Fay", "Gus", "Hana"]
NORMAL = [
    ("Charged twice for one order", "I was charged twice for order 1042. Please refund one payment."),
    ("How do I change the colour theme?", "Is there a dark mode in the settings page?"),
    ("Export to CSV fails", "The export button shows an error after I pick a date range."),
    ("Cannot reset my password", "The reset email never arrives, I checked spam too."),
    ("Invoice shows the wrong address", "Our invoice still has our old office address."),
    ("App crashes on login", "After the last update the app closes as soon as I sign in."),
    ("Feature idea: weekly summary", "A weekly email with the ticket counts would help our team."),
]
EDGE = [
    ("Empty body", ""),
    ("Très lent le matin", "L'application est très lente le matin. Pouvez-vous regarder ?"),
    ("Thanks \U0001F389", "Everything works now \U0001F44D"),
    ("Long ticket", "The page freezes when I scroll. " * 40),
]


def build():
    rng = random.Random(SEED)
    rows = NORMAL + EDGE
    rows.append(NORMAL[0])  # a duplicate of the first ticket
    rng.shuffle(rows)
    return [
        {"id": i + 1, "customer": rng.choice(CUSTOMERS), "subject": s, "body": b}
        for i, (s, b) in enumerate(rows)
    ]


def dump(tickets):
    return json.dumps(tickets, indent=1, ensure_ascii=False) + "\n"


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    text = dump(build())
    if args.check:
        if not OUT.is_file():
            print(f"Cannot find {OUT}. Run python3 seed_data.py first.")
            sys.exit(2)
        same = OUT.read_text(encoding="utf-8") == text
        print(f"{OUT} matches the seed: {'yes' if same else 'NO'} (hash {digest(text)})")
        sys.exit(0 if same else 1)
    OUT.write_text(text, encoding="utf-8")
    empty = sum(1 for t in json.loads(text) if not t["body"])
    print(f"Wrote {len(json.loads(text))} tickets to {OUT} (seed {SEED}, hash {digest(text)}, {empty} with an empty body)")


if __name__ == "__main__":
    main()
