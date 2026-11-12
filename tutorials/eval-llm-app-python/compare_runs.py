"""Compare two saved results files, case by case."""
import json
import sys
from pathlib import Path

a, b = (json.loads(Path(p).read_text()) for p in sys.argv[1:3])
print(f"{sys.argv[1]}: pass rate {a['pass_rate']:.0f}%")
print(f"{sys.argv[2]}: pass rate {b['pass_rate']:.0f}%")
changed = 0
for x, y in zip(a["results"], b["results"]):
    if x["passed"] != y["passed"]:
        changed += 1
        print(f"  {x['id']}: {'pass' if x['passed'] else 'fail'} -> {'pass' if y['passed'] else 'fail'}")
same_text = sum(x["reply"] == y["reply"] for x, y in zip(a["results"], b["results"]))
print(f"cases whose verdict changed: {changed}")
print(f"cases with word-for-word identical replies: {same_text} of {len(a['results'])}")
