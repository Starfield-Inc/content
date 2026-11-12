"""Check the scoring rule on fixed answers. No API call. Run: python test_score.py"""
from score import is_correct, normalise

CASES = [
    ("408", ["408"], True),
    ("  408.  ", ["408"], True),
    ("1,000", ["1000"], True),
    ("Canberra", ["canberra"], True),
    ("'maerts'", ["maerts"], True),
    ("Three", ["3", "three"], True),
    ("The answer is 408", ["408"], False),
    ("409", ["408"], False),
    ("Sydney", ["canberra"], False),
    ("", ["5"], False),
]

for answer, accept, expected in CASES:
    got = is_correct(answer, accept)
    assert got == expected, f"{answer!r} vs {accept}: expected {expected}, got {got}"
    print(f"{'correct' if got else 'wrong  '}  {answer!r:<22} accepted {accept}  (normalised {normalise(answer)!r})")
print(f"all {len(CASES)} scoring checks passed")
