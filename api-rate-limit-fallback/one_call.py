"""One real API call. Prints the reply and saves it as the fallback answer."""
import json
import os
import sys

from anthropic import Anthropic

from prompt import MAX_TOKENS, MODEL, PROMPT
from spend_log import log_usage

if not os.environ.get("ANTHROPIC_API_KEY"):
    sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env before you run this.")

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment
print("client.max_retries:", client.max_retries)

response = client.messages.create(
    model=MODEL,
    max_tokens=MAX_TOKENS,
    thinking={"type": "disabled"},
    messages=[{"role": "user", "content": PROMPT}],
)
log_usage("one_call.py", response)

text = "".join(block.text for block in response.content if block.type == "text")
print("reply:", text)
print("input tokens:", response.usage.input_tokens)
print("output tokens:", response.usage.output_tokens)

with open("saved_answer.json", "w") as f:
    json.dump({"prompt": PROMPT, "text": text}, f)
print("saved saved_answer.json")
