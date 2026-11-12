import json
import time
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:8042"


def post(body):
    req = urllib.request.Request(BASE + "/compare", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    return urllib.request.urlopen(req, timeout=60)


for _ in range(60):  # wait for the server
    try:
        urllib.request.urlopen(BASE + "/?demo=0", timeout=2)
        break
    except OSError:
        time.sleep(0.5)

try:
    post({"prompt": ""})
    raise SystemExit("an empty prompt was accepted")
except urllib.error.HTTPError as e:
    assert e.code == 422, e.code
    print("empty prompt rejected with 422")

data = json.load(post({"prompt": "Name one use of a rate limit, in ten words or fewer."}))
results = data["results"]
assert len(results) == 2 and all(r["answer"] for r in results)
for r in results:
    print(r["label"], r["output_tokens"], "output tokens")
print("route returned 2 columns")
