import argparse
import json
import sys
from pathlib import Path

WORDS_PER_MINUTE = 130


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("deck_json")
    parser.add_argument("--limit", type=int, default=180, help="time limit in seconds")
    args = parser.parse_args()

    path = Path(args.deck_json)
    if not path.is_file():
        sys.exit(f"Cannot find {path}")
    slides = json.loads(path.read_text())["slides"]

    total = 0.0
    for i, slide in enumerate(slides, 1):
        words = len(slide["notes"].split())
        seconds = words / WORDS_PER_MINUTE * 60
        total += seconds
        print(f"{i}. {slide['title']:<14} {words:>3} words  {seconds:>4.0f} s")
    print(f"Total {total:.0f} s at {WORDS_PER_MINUTE} words per minute, limit {args.limit} s")
    if total > args.limit:
        print(f"Over by {total - args.limit:.0f} s. Cut words from the notes.")
        sys.exit(1)
    print("Fits.")


if __name__ == "__main__":
    main()
