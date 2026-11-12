import hashlib
import json
import time
from pathlib import Path

from anthropic import Anthropic

MODEL = "claude-haiku-5-5"
MAX_TOKENS = 300
SYSTEM = "You are a concise tutor. Answer in one or two short sentences."


def make_key(model, max_tokens, thinking, system, question, normalize=False):
    """Hash every field that can change the answer. Same fields, same key."""
    if normalize:
        question = " ".join(question.split()).lower()
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "thinking": thinking,
        "system": system,
        "question": question,
    }
    text = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def reply_text(response):
    """Join the text blocks. A reply can hold only a thinking block and no text."""
    return "".join(b.text for b in response.content if b.type == "text").strip()


class Cache:
    def __init__(self, path, ttl_seconds=3600):
        self.path = Path(path)
        self.ttl = ttl_seconds
        self.entries = json.loads(self.path.read_text()) if self.path.exists() else {}

    def get(self, key):
        entry = self.entries.get(key)
        if entry is None:
            return None
        if time.time() - entry["saved_at"] > self.ttl:
            del self.entries[key]  # expired: treat as a miss
            return None
        return entry

    def put(self, key, text, usage):
        if not text:
            return  # never cache an empty reply
        self.entries[key] = {"text": text, "usage": usage, "saved_at": time.time()}
        self.path.write_text(json.dumps(self.entries, indent=1))


def ask(cache, client, question, normalize=False, model=MODEL, max_tokens=MAX_TOKENS, thinking="disabled"):
    """Return (text, hit, usage, seconds). A hit makes no API call."""
    start = time.perf_counter()
    key = make_key(model, max_tokens, thinking, SYSTEM, question, normalize)
    entry = cache.get(key)
    if entry:
        return entry["text"], True, entry["usage"], time.perf_counter() - start
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=SYSTEM,
        thinking={"type": thinking},
        messages=[{"role": "user", "content": question}],
    )
    text = reply_text(response)
    usage = {"input": response.usage.input_tokens, "output": response.usage.output_tokens}
    cache.put(key, text, usage)
    return text, False, usage, time.perf_counter() - start


def make_client():
    return Anthropic()
