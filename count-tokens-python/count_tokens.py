import argparse
import sys
from pathlib import Path

import tiktoken

ENCODINGS = ["cl100k_base", "o200k_base"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Count the tokens in a text file.")
    parser.add_argument("path", help="the text file to count")
    parser.add_argument("--price-per-million", type=float,
                        help="price in dollars per million input tokens, copied from your provider's price page")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.is_file():
        print(f"Cannot find {path}. Check the file name and try again.", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")
    print(f"File:       {path}")
    print(f"Characters: {len(text):,}")
    print(f"Words:      {len(text.split()):,}")
    print()
    print(f"{'Encoding':<14}{'Tokens':>8}", end="")
    print(f"{'Cost':>12}" if args.price_per_million is not None else "")
    for name in ENCODINGS:
        count = len(tiktoken.get_encoding(name).encode(text))
        line = f"{name:<14}{count:>8,}"
        if args.price_per_million is not None:
            line += f"{'$' + format(count / 1_000_000 * args.price_per_million, '.6f'):>12}"
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
