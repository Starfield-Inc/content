"""Stream one answer from the model and time it. Saves the chunks to cache.json."""
import json
import os
import sys
import time

from anthropic import Anthropic

from prompt import MAX_TOKENS, MODEL, PROMPT
from spend_log import log_usage

if not os.environ.get("ANTHROPIC_API_KEY"):
    sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env before you run this.")

client = Anthropic()
chunks = []
start = time.perf_counter()

with client.messages.stream(
    model=MODEL,
    max_tokens=MAX_TOKENS,
    thinking={"type": "disabled"},
    messages=[{"role": "user", "content": PROMPT}],
) as stream:
    for text in stream.text_stream:
        chunks.append({"t": round(time.perf_counter() - start, 3), "text": text})
    final = stream.get_final_message()

log_usage("timing.py", final)

opening, last = chunks[0]["t"], chunks[-1]["t"]
print("answer:", "".join(c["text"] for c in chunks))
print(f"chunks: {len(chunks)}")
print(f"opening chunk after {opening:.2f} s")
print(f"last chunk after {last:.2f} s")
print(f"a reader of a non-streaming page would see nothing for {last:.2f} s; this reader sees text after {opening:.2f} s")

with open("cache.json", "w") as f:
    json.dump({"prompt": PROMPT, "chunks": chunks}, f)
print("saved cache.json")
