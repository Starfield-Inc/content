import json
import os
import sys
import time

import anthropic

from models import MAX_TOKENS, MODELS, cost_usd
from spend_log import log_usage


def ask(client, model, prompt):
    """Send the prompt to one model. Return the answer and what the call cost."""
    start = time.perf_counter()
    response = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        thinking=MODELS[model]["thinking"],
        messages=[{"role": "user", "content": prompt}],
    )
    seconds = time.perf_counter() - start
    log_usage("compare.py", model, response.usage)
    return {
        "model": model,
        "label": MODELS[model]["label"],
        "answer": "".join(block.text for block in response.content if block.type == "text"),
        "seconds": round(seconds, 2),
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "cost_usd": cost_usd(model, response.usage.input_tokens, response.usage.output_tokens),
    }


def compare(client, prompt):
    # One after the other, so the two timings do not compete for the same connection.
    return [ask(client, model, prompt) for model in MODELS]


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--save"]
    if not args:
        sys.exit('Usage: python compare.py "your prompt" [--save file.json]')
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env before running this.")
    prompt = args[0]
    results = compare(anthropic.Anthropic(), prompt)
    for r in results:
        print(f"== {r['label']}")
        print(r["answer"])
        print(f"{r['seconds']} seconds, {r['input_tokens']} input tokens, "
              f"{r['output_tokens']} output tokens, cost ${r['cost_usd']:.6f}")
        print()
    if "--save" in sys.argv:
        path = args[1]
        with open(path, "w") as f:
            json.dump({"prompt": prompt, "results": results}, f, indent=2)
        print(f"saved to {path}")
