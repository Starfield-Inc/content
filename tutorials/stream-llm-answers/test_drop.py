"""Drop the connection after 4 events, then resume with Last-Event-ID, like a browser does."""
import json
import sys
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:8041/demo"


def read_events(url, last_id=None):
    """Return a list of (event_id, event_name, data) read until the response ends."""
    headers = {"Last-Event-ID": str(last_id)} if last_id is not None else {}
    events = []
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:
        block = {}
        for raw in response:
            line = raw.decode().rstrip("\n")
            if line:
                key, _, value = line.partition(": ")
                block[key] = value
            elif block:
                events.append((block.get("id"), block.get("event", "message"), json.loads(block["data"])))
                block = {}
    return events


opening = read_events(f"{BASE}?speed=0&drop_after=4")
texts = [d for _, name, d in opening if name == "message"]
print(f"opening connection: {len(texts)} events, last id {opening[-1][0]}")
if any(name == "done" for _, name, _ in opening):
    sys.exit("expected the connection to end early")
print("connection ended with no done event")

last_id = opening[-1][0]
rest = read_events(f"{BASE}?speed=0&drop_after=4", last_id=last_id)
print(f"resumed after event {last_id}: {len(rest)} more events, starting id {rest[0][0]}, last is '{rest[-1][1]}'")

texts += [d for _, name, d in rest if name == "message"]
saved = "".join(c["text"] for c in json.load(open("cache.json"))["chunks"])
same = "".join(texts) == saved
print(f"joined text matches the saved answer: {'yes' if same else 'no'}")
sys.exit(0 if same else 1)
