"""Ask every question to both models and save the raw answers, tokens and time to results.json."""
import json
import os
import sys
import time

import anthropic

from models import MAX_TOKENS, MODELS, cost_usd
from spend_log import log_usage

INSTRUCTION = "Reply with only the final answer. No explanation, no working."


def ask(client, model, question):
    start = time.perf_counter()
    response = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        thinking=MODELS[model]["thinking"],
        messages=[{"role": "user", "content": f"{question}\n\n{INSTRUCTION}"}],
    )
    seconds = time.perf_counter() - start
    log_usage("run_eval.py", model, response.usage)
    answer = "".join(b.text for b in response.content if b.type == "text")
    return {"answer": answer, "seconds": seconds,
            "input_tokens": response.usage.input_tokens, "output_tokens": response.usage.output_tokens}


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env before running this.")
    questions = json.load(open("questions.json"))
    client = anthropic.Anthropic()
    data = {"models": {}}
    for model in MODELS:  # one model after the other, one question after the other
        rows = {str(q["id"]): ask(client, model, q["question"]) for q in questions}
        totals = {k: sum(r[k] for r in rows.values()) for k in ("seconds", "input_tokens", "output_tokens")}
        data["models"][model] = {"label": MODELS[model]["label"], "answers": rows, **totals,
                                 "cost_usd": cost_usd(model, totals["input_tokens"], totals["output_tokens"])}
        print(f"{MODELS[model]['label']}: asked {len(rows)} questions")
    json.dump(data, open("results.json", "w"), indent=2)
    print("saved results.json")


if __name__ == "__main__":
    main()
