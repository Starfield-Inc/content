import os
import sys

from anthropic import Anthropic

from spend_log import log_usage

MODEL = "claude-haiku-5-5"
MAX_TOKENS = 100

if not os.environ.get("ANTHROPIC_API_KEY"):
    sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env first.")

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment


def ask(messages):
    response = client.messages.create(model=MODEL, max_tokens=MAX_TOKENS, messages=messages)
    log_usage("forgetful.py", response)
    # A reply can hold other blocks, such as a thinking block, so join only the text blocks.
    return "".join(block.text for block in response.content if block.type == "text")


# Two separate calls. The second call sends only the new question.
print("you> My name is Maya.")
print("bot>", ask([{"role": "user", "content": "My name is Maya. Reply in one short sentence."}]))
print("you> What is my name?")
print("bot>", ask([{"role": "user", "content": "What is my name? Reply in one short sentence."}]))
