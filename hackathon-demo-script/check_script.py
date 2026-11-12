"""Estimate how long a demo script takes to say, beat by beat.

Beats are `## Name (20s)` headings. Lines starting with `>` are notes for the screen
and are not spoken, so they are not counted. The speaking rate is an assumption
(default 130 words a minute). Time yourself once and pass your own rate with --wpm.
"""
import argparse
import re
import sys
from pathlib import Path

BEAT = re.compile(r"^##\s+(.+?)\s*\((\d+)s\)\s*$")


def read_beats(path):
    beats = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        m = BEAT.match(line.strip())
        if m:
            beats.append({"name": m.group(1), "budget": int(m.group(2)), "words": 0})
        elif beats and line.strip() and not line.startswith(">"):
            beats[-1]["words"] += len(line.split())
    return beats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--wpm", type=int, default=130, help="words you speak per minute")
    ap.add_argument("--limit", type=int, default=180, help="slot length in seconds")
    args = ap.parse_args()
    if not Path(args.script).is_file():
        print(f"Cannot find {args.script}")
        sys.exit(2)
    beats = read_beats(args.script)
    if not beats:
        print("No beats found. Use headings like: ## Hook (20s)")
        sys.exit(2)
    total = 0.0
    for b in beats:
        secs = b["words"] / args.wpm * 60
        total += secs
        flag = "OVER BUDGET" if secs > b["budget"] else "ok"
        print(f"{b['name']:<22} {b['words']:>4} words  {secs:5.1f}s of {b['budget']:>3}s  {flag}")
    print(f"Total: {total:.0f}s spoken at {args.wpm} words a minute. Slot: {args.limit}s.")
    if total > args.limit:
        print(f"Too long by {total - args.limit:.0f}s. Cut words before you rehearse.")
        sys.exit(1)
    print(f"Fits, with {args.limit - total:.0f}s to spare.")


if __name__ == "__main__":
    main()
