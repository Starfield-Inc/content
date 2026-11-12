"""One small helper that sends a prompt to the model and logs the tokens used."""
import os, sys, time
from pathlib import Path

import anthropic

MODEL = "claude-haiku-5-5"
MAX_TOKENS = 300
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


def ask(prompt):
    response = get_client().messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        thinking={"type": "disabled"},  # plain answers, no reasoning tokens
        messages=[{"role": "user", "content": prompt}],
    )
    with SPEND_LOG.open("a") as log:
        log.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {MODEL} in={response.usage.input_tokens} out={response.usage.output_tokens}\n")
    return "".join(b.text for b in response.content if b.type == "text").strip()
