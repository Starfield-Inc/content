"""Compare your real rehearsal times with the plan.

Time each beat with a phone stopwatch, then pass the seconds in beat order:
    python3 rehearse.py demo_script.md --times 22,28,70,24,21
Each beat is compared with its budget, and the total with the slot.
"""
import argparse
import sys

from check_script import read_beats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--times", required=True, help="seconds per beat, comma separated")
    ap.add_argument("--limit", type=int, default=180)
    args = ap.parse_args()
    beats = read_beats(args.script)
    times = [float(t) for t in args.times.split(",")]
    if len(times) != len(beats):
        print(f"The script has {len(beats)} beats but you gave {len(times)} times.")
        sys.exit(2)
    for b, t in zip(beats, times):
        print(f"{b['name']:<22} {t:5.0f}s of {b['budget']:>3}s  {'ok' if t <= b['budget'] else 'over by %.0fs' % (t - b['budget'])}")
    total = sum(times)
    print(f"Total: {total:.0f}s. Slot: {args.limit}s. Spare: {args.limit - total:.0f}s.")
    if total > args.limit - 10:
        print("Less than 10s spare. Cut something before demo day.")
        sys.exit(1)
    print("Leaves at least 10s spare.")


if __name__ == "__main__":
    main()
