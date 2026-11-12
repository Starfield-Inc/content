"""Fixed-data check of the cache rules. No API call: a stub stands in for the client."""
import tempfile
import time
from pathlib import Path
from types import SimpleNamespace as NS

from llm_cache import Cache, ask


class Stub:
    def __init__(self, blocks):
        self.blocks = blocks
        self.calls = 0
        self.messages = self

    def create(self, **kw):
        self.calls += 1
        return NS(content=self.blocks, usage=NS(input_tokens=5, output_tokens=0))


tmp = Path(tempfile.mkdtemp())
cache = Cache(tmp / "c.json")
empty = Stub([NS(type="thinking", text=None)])
ask(cache, empty, "q")
ask(cache, empty, "q")
assert empty.calls == 2, "an empty reply must not be cached"
print("empty reply: not cached, 2 calls for 2 asks")

good = Stub([NS(type="text", text="hello")])
ask(cache, good, "q")
ask(cache, good, "q")
assert good.calls == 1
print("good reply: cached, 1 call for 2 asks")

short = Cache(tmp / "s.json", ttl_seconds=0.2)
ask(short, good, "z")
time.sleep(0.3)
ask(short, good, "z")
assert good.calls == 3
print("expired entry: called again")
print("all checks passed")
