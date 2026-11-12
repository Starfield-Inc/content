"""Fixed-data check of the two code-side tests. No API call."""
import sys
sys.argv = ["x"]
src = open("check_summary.py").read().split("\nmain()")[0]
exec(src)

SOURCE = "The repair cost 22,500 euros. The council has not promised funding beyond 2027."

cases = [
    ("repair cost 22,500 euros", {"quote": "The repair cost 22,500 euros.", "supports": True}, "found"),
    ("repair cost 25,200 euros", {"quote": "The repair cost 22,500 euros.", "supports": True}, "NOT FOUND"),
    ("a quote made up by the model", {"quote": "The repair was free.", "supports": True}, "NOT FOUND"),
    ("no sentence at all", {"quote": None, "supports": False}, "NOT FOUND"),
    ("funding is promised beyond 2027", {"quote": "The council has not promised funding beyond 2027.", "supports": True}, "found"),
]
for claim, answer, expected in cases:
    status, reason = judge(claim, answer, SOURCE)
    assert status == expected, (claim, status, reason)
    print(f"ok: {claim!r} -> {status}")
print("Last case passes as 'found' on purpose: the code cannot read meaning. It is a known miss.")
