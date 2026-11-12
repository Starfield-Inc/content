import argparse
import os
import sys

from llm_cache import MAX_TOKENS, Cache, ask, make_client

parser = argparse.ArgumentParser()
parser.add_argument("questions")
parser.add_argument("--cache", default="cache.json")
parser.add_argument("--ttl", type=float, default=3600)
parser.add_argument("--max-tokens", type=int, default=MAX_TOKENS)
parser.add_argument("--normalize", action="store_true")
parser.add_argument("--limit", type=int, default=0, help="only the first N questions")
args = parser.parse_args()

if not os.environ.get("ANTHROPIC_API_KEY"):
    sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env first.")

lines = [l for l in open(args.questions).read().split("\n") if l.strip()]
if args.limit:
    lines = lines[: args.limit]

cache = Cache(args.cache, args.ttl)
client = make_client()
calls = hits = 0
spent_in = spent_out = saved_in = saved_out = 0
total_seconds = 0.0
for i, q in enumerate(lines, 1):
    text, hit, usage, secs = ask(cache, client, q, args.normalize, max_tokens=args.max_tokens)
    total_seconds += secs
    if hit:
        hits += 1
        saved_in += usage["input"]
        saved_out += usage["output"]
    else:
        calls += 1
        spent_in += usage["input"]
        spent_out += usage["output"]
    tag = "HIT " if hit else "MISS"
    print(f"{i} {tag} {secs * 1000:7.1f} ms  in={usage['input']} out={usage['output']}  {q.strip()[:34]}")

print()
print(f"questions: {len(lines)}  API calls: {calls}  cache hits: {hits}")
print(f"tokens sent to the API: input {spent_in}, output {spent_out}")
print(f"tokens not sent thanks to hits: input {saved_in}, output {saved_out}")
print(f"total time: {total_seconds:.2f} s")
