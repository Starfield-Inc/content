"""Call the running app's endpoint the way the page does. Needs the app on port 8125."""
import json
import sys
import urllib.error
import urllib.request

from drafts import BAD, GOOD, INJECTION
from safety import MAX_DRAFT_CHARS

URL = "http://127.0.0.1:8125/api/suggest"


def post(draft):
    req = urllib.request.Request(URL, json.dumps({"draft": draft}).encode(), {"content-type": "application/json"})
    try:
        with urllib.request.urlopen(req) as res:
            return res.status, json.load(res)
    except urllib.error.HTTPError as err:
        return err.code, json.load(err)


cases = [
    ("good draft", GOOD),
    ("harmful request", BAD),
    ("empty draft", "   "),
    ("too long", "a" * (MAX_DRAFT_CHARS + 1)),
]
if "--injection" in sys.argv:
    cases = [("injection", INJECTION)]
for name, draft in cases:
    status, data = post(draft)
    print(f"--- {name}: HTTP {status}")
    print(json.dumps(data, indent=2))
