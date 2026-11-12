import json
import os
import sys

from anthropic import Anthropic
from pydantic import ValidationError

from schema import Ticket

MODEL = os.environ.get("TUTORIAL_MODEL", "claude-haiku-5-5")
MAX_TOKENS = 400

# A strict prompt: it names every field and every allowed value.
STRICT = (
    "Read the support message and reply with one JSON object and nothing else. "
    'Keys: "category" (one of billing, bug, question, feature), "priority" (integer 1 to 5, '
    '5 is most urgent), "summary" (at most 60 characters), "needs_human" (true or false). '
    "No markdown, no code fence."
)
# A loose prompt: it asks for JSON but does not say which values are allowed.
LOOSE = (
    "Read the support message and reply with a JSON object with the keys category, "
    "priority, summary and needs_human. Reply with JSON only."
)


def call(client, system, messages):
    # No thinking: with thinking on and a small max_tokens the reply can hold only a thinking block.
    response = client.messages.create(model=MODEL, max_tokens=MAX_TOKENS, system=system, messages=messages)
    return "".join(b.text for b in response.content if b.type == "text")


def check(raw):
    """Return (Ticket, None) or (None, error text). Never raises on bad model output."""
    if not raw.strip():
        return None, "The reply was empty."
    try:
        return Ticket.model_validate_json(raw), None
    except ValidationError as err:
        return None, "; ".join(f"{'.'.join(map(str, e['loc'])) or 'json'}: {e['msg']}" for e in err.errors())


def ask_json(client, system, text, retries=1):
    """Ask for a Ticket. Returns (ticket or None, attempts, list of (raw, error))."""
    messages = [{"role": "user", "content": text}]
    failures = []
    for attempt in range(1, retries + 2):
        raw = call(client, system, messages)
        ticket, error = check(raw)
        if ticket:
            return ticket, attempt, failures
        failures.append((raw, error))
        messages += [
            {"role": "assistant", "content": raw or "(empty)"},
            {"role": "user", "content": "That reply failed validation:\n" + error + "\nReply again with corrected JSON only."},
        ]
    return None, retries + 1, failures


def client_or_exit():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env first.")
    return Anthropic()
