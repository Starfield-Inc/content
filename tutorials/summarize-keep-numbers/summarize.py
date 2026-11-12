import argparse
import os
import sys
from pathlib import Path

from anthropic import Anthropic

from chunks import split_text
from numcheck import read, report

MODEL = "claude-haiku-5-5"
MAX_TOKENS = 600
RULES = "Keep every number exactly as written in the text. Do not round, convert or recompute any number."


def reply_text(response):
    """Join the text blocks. A reply can also hold other blocks, such as a thinking block."""
    return "".join(block.text for block in response.content if block.type == "text")


def ask(client, prompt, usage):
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        thinking={"type": "disabled"},  # with thinking on, a small max_tokens can be spent before any text
        messages=[{"role": "user", "content": prompt}],
    )
    usage[0] += response.usage.input_tokens
    usage[1] += response.usage.output_tokens
    text = reply_text(response).strip()
    if not text:
        sys.exit(f"The model returned no text (stop reason: {response.stop_reason}).")
    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--max-chars", type=int, default=900, help="size of each chunk")
    parser.add_argument("--words", type=int, default=150, help="length of the final summary")
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env first.")
    text = read(args.file)
    client = Anthropic()
    usage = [0, 0]

    parts = split_text(text, args.max_chars)
    partials = []
    for number, part in enumerate(parts, 1):
        prompt = f"Summarise this part of a report in at most 60 words. {RULES}\n\n{part}"
        partials.append(ask(client, prompt, usage))
        print(f"chunk {number}/{len(parts)} summarised")

    merged = "\n\n".join(partials)
    prompt = (
        f"These are summaries of consecutive parts of one report. Merge them into one summary "
        f"of at most {args.words} words. {RULES}\n\n{merged}"
    )
    summary = ask(client, prompt, usage)
    Path("summary.txt").write_text(summary + "\n", encoding="utf-8")

    print(f"\nSummary ({len(summary.split())} words):\n{summary}\n")
    report(text, summary)
    print(f"[tokens used: input {usage[0]}, output {usage[1]}]")


if __name__ == "__main__":
    main()
