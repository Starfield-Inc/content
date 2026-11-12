import os
import sys

from anthropic import Anthropic, BadRequestError

from llm_cache import MODEL

if not os.environ.get("ANTHROPIC_API_KEY"):
    sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env first.")

client = Anthropic()
try:
    client.messages.create(
        model=MODEL,
        max_tokens=50,
        thinking={"type": "disabled"},
        messages=[{"role": "user", "content": "Say hi."}],
        extra_body={"temperature": 0.0},  # the SDK method has no temperature argument
    )
    print("temperature accepted: add it to make_key")
except BadRequestError as err:
    print(f"HTTP {err.status_code}: {err.body['error']['message']}")
    print("temperature is not a setting for this model, so it is not in the key")
