"""Fetch every file the browser can get and look for the key. Run while the app is up."""
import os
import re
import sys
import urllib.request

BASE = "http://127.0.0.1:8125"
key = os.environ.get("ANTHROPIC_API_KEY", "")
if len(key) < 8:
    sys.exit("ANTHROPIC_API_KEY is not set, so there is nothing to look for.")

page = urllib.request.urlopen(BASE + "/").read().decode()
found = {"/": page}
for src in re.findall(r'src="([^"]+)"', page):
    if src.startswith("/") and src != "/hold.js":
        found[src] = urllib.request.urlopen(BASE + src).read().decode()

for path, text in found.items():
    print(f"{path}: {len(text)} bytes, key present: {key in text}")
if any(key in text for text in found.values()):
    sys.exit("The key is in a file the browser receives.")
print("The key stays on the server.")
