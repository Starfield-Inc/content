import os
import sys

from anthropic import Anthropic

from spend_log import log_usage

MODEL = "claude-haiku-5-5"
MAX_TOKENS = 200

if not os.environ.get("ANTHROPIC_API_KEY"):
    sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env first.")

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment

response = client.messages.create(
    model=MODEL,
    max_tokens=MAX_TOKENS,
    messages=[{"role": "user", "content": "Suggest a name for a hackathon chatbot that answers questions about recycling. Reply with the name only."}],
)
log_usage("one_call.py", response)

# A reply is a list of blocks. Join the text blocks.
print("reply:", "".join(block.text for block in response.content if block.type == "text"))
print("input tokens:", response.usage.input_tokens)
print("output tokens:", response.usage.output_tokens)
