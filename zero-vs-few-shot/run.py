import csv
import json
import os
import sys

import anthropic

from prompts import build_prompt
from spend_log import log_usage

MODEL = "claude-haiku-5-5"
MAX_TOKENS = 10


def run(mode, client):
    """Send each input once with this mode's prompt. Save the raw replies."""
    results = []
    for row in csv.DictReader(open("inputs.csv")):
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            thinking={"type": "disabled"},
            messages=[{"role": "user", "content": build_prompt(mode, row["text"])}],
        )
        log_usage("run.py", response)
        raw = "".join(block.text for block in response.content if block.type == "text")
        results.append({"id": int(row["id"]), "text": row["text"], "expected": row["expected"], "raw": raw,
                        "input_tokens": response.usage.input_tokens, "output_tokens": response.usage.output_tokens})
    with open(f"results_{mode}.json", "w") as f:
        json.dump(results, f, indent=2)
    return results


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode not in ("zero", "few"):
        sys.exit("Usage: python run.py zero|few")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env before running this.")
    results = run(mode, anthropic.Anthropic())
    print(f"{mode}-shot: {len(results)} calls, saved to results_{mode}.json")
    print("input tokens:", sum(r["input_tokens"] for r in results))
    print("output tokens:", sum(r["output_tokens"] for r in results))
