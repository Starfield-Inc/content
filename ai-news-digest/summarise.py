import argparse
import json
import os
import sys
from pathlib import Path

from anthropic import Anthropic

from spend_log import log_usage

MODEL = os.environ.get("TUTORIAL_MODEL", "claude-haiku-5-5")
MAX_TOKENS = 120
SYSTEM = (
    "You write one-sentence news summaries. Use only the title and text you are given. "
    "Do not add facts, names or numbers that are not in them. "
    "If the text is too thin to summarise, reply exactly: Not enough text to summarise."
)


def summarise(client: Anthropic, item: dict) -> str:
    prompt = f"Title: {item['title']}\n\nText: {item['text'] or '(no text in the feed)'}"
    response = client.messages.create(
        model=MODEL, max_tokens=MAX_TOKENS, system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    log_usage("summarise.py", response)
    return "".join(b.text for b in response.content if b.type == "text").strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("infile")
    parser.add_argument("outfile")
    parser.add_argument("--limit", type=int, default=6)
    parser.add_argument("--quiet", action="store_true", help="print counts only, not titles or summaries")
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env first.")
    client = Anthropic()

    items = json.loads(Path(args.infile).read_text())[: args.limit]
    done = []
    for n, item in enumerate(items, 1):
        # The link comes from the feed item, never from the model, so it cannot be invented.
        done.append({**item, "summary": summarise(client, item)})
        if not args.quiet:
            print(f"{n}. {item['title']}\n   {done[-1]['summary']}\n   {item['link']}\n")
    Path(args.outfile).write_text(json.dumps(done, indent=2), encoding="utf-8")
    print(f"Summarised {len(done)} items with {MODEL}. Saved to {args.outfile}")


if __name__ == "__main__":
    main()
