import os
import sys
import time

from llm_cache import Cache, ask, make_client

if not os.environ.get("ANTHROPIC_API_KEY"):
    sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env first.")

cache = Cache("cache-expiry.json", ttl_seconds=2)
client = make_client()
q = "What is a context window?"

for label in ("first ask", "right away", "after 3 s wait"):
    if label == "after 3 s wait":
        time.sleep(3)
    _, hit, _, secs = ask(cache, client, q)
    print(f"{label:15} {'HIT ' if hit else 'MISS'} {secs * 1000:7.1f} ms  (ttl 2 s)")
