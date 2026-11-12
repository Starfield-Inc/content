"""Print every failing case from a saved results file: the message, why it failed, and the reply."""
import json
import sys
from pathlib import Path

cases = {c["id"]: c for c in json.loads(Path("cases.json").read_text())}
data = json.loads(Path(sys.argv[1]).read_text())
for r in data["results"]:
    if r["passed"]:
        continue
    print(f"Case: {r['id']}")
    print(f"Customer: {cases[r['id']]['message']}")
    print("Why it failed: " + "; ".join(r["problems"]))
    print(f"Reply: {r['reply']}\n")
