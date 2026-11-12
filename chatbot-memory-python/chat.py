import argparse
import os
import sys

from anthropic import Anthropic

from spend_log import log_usage

MODEL = "claude-haiku-5-5"
MAX_TOKENS = 150
SYSTEM = "You are a friendly assistant. Answer in one or two short sentences."

LETTER = {"user": "U", "assistant": "A"}


def reply_text(response):
    """Join the text blocks. A reply can also hold other blocks, such as a thinking block."""
    return "".join(block.text for block in response.content if block.type == "text")


def trim(messages, keep):
    """Keep the last `keep` messages (0 means keep all), starting on a user turn."""
    kept = messages[-keep:] if keep else messages
    while kept and kept[0]["role"] != "user":
        kept = kept[1:]
    return kept


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keep", type=int, default=0, help="keep only the last N messages (0 = all)")
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env first.")
    client = Anthropic()

    messages = []
    total_in = total_out = 0
    while True:
        try:
            line = input("you> ")
        except EOFError:
            break
        if not sys.stdin.isatty():
            print(line)  # a piped line is not echoed by a terminal, so print it
        if not line.strip():
            continue

        messages.append({"role": "user", "content": line})
        before = len(messages)
        messages = trim(messages, args.keep)
        if len(messages) < before:
            print(f"[trimmed {before - len(messages)} old messages]")

        response = client.messages.create(model=MODEL, max_tokens=MAX_TOKENS, system=SYSTEM, messages=messages)
        log_usage("chat.py", response)
        reply = reply_text(response)
        usage = response.usage
        total_in += usage.input_tokens
        total_out += usage.output_tokens

        letters = " ".join(LETTER[m["role"]] for m in messages)
        print(f"bot> {reply}")
        print(f"[sent {len(messages)} messages: {letters} | input tokens {usage.input_tokens}, output tokens {usage.output_tokens}]")
        messages.append({"role": "assistant", "content": reply})

    print()
    print(f"[session total: input tokens {total_in}, output tokens {total_out}]")


main()
