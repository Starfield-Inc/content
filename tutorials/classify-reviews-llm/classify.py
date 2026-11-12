"""Classify reviews as positive, negative or mixed with one API call per review.

  python classify.py --text "Some review"      one review, prints the label
  python classify.py --prompt v1               all of reviews.csv, saves results_v1.csv
"""
import argparse, csv, os, sys, time
from pathlib import Path

import anthropic

from prompts import LABELS, PROMPTS

MODEL = "claude-haiku-5-5"
MAX_TOKENS = 10  # a label is one word
SPEND_LOG = Path("spend.log")


def get_client():
    if not os.environ.get("ANTHROPIC_API_KEY") and Path(".env").is_file():
        for line in Path(".env").read_text().splitlines():
            if line.startswith("ANTHROPIC_API_KEY="):
                os.environ["ANTHROPIC_API_KEY"] = line.split("=", 1)[1].strip()
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY is not set. Put it in a .env file or export it in your terminal.")
        sys.exit(2)
    return anthropic.Anthropic()


def classify(client, prompt_name, review):
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        thinking={"type": "disabled"},  # no reasoning tokens: the answer is one word
        messages=[{"role": "user", "content": PROMPTS[prompt_name].format(review=review)}],
    )
    with SPEND_LOG.open("a") as log:
        log.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {MODEL} in={response.usage.input_tokens} out={response.usage.output_tokens}\n")
    raw = "".join(b.text for b in response.content if b.type == "text").strip()
    words = raw.lower().split()
    word = words[0].strip(".,!:;\"'") if words else ""
    return (word if word in LABELS else "invalid"), raw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", default="v1", choices=sorted(PROMPTS))
    parser.add_argument("--text")
    parser.add_argument("--input", default="reviews.csv")
    args = parser.parse_args()
    client = get_client()
    if args.text:
        label, raw = classify(client, args.prompt, args.text)
        print(f"Review: {args.text}")
        print(f"Predicted: {label}")
        return
    rows = list(csv.DictReader(open(args.input, newline="")))
    out_path = f"results_{args.prompt}.csv"
    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "text", "label", "predicted", "raw"])
        for row in rows:
            predicted, raw = classify(client, args.prompt, row["text"])
            writer.writerow([row["id"], row["text"], row["label"], predicted, raw])
    print(f"Classified {len(rows)} reviews with prompt {args.prompt}. Saved {out_path}")


if __name__ == "__main__":
    main()
