"""Checks with fixed numbers and a fake clock. No API call is made."""
from datetime import date

from limits import DailyCap, RateLimiter, cost_usd

now = [0.0]
r = RateLimiter(limit=2, window=60, clock=lambda: now[0])
assert r.allow("a") == 0 and r.allow("a") == 0
assert r.allow("a") > 0, "third request in the window must wait"
assert r.allow("b") == 0, "another user has its own count"
now[0] = 61
assert r.allow("a") == 0, "the window has passed"

day = [date(2026, 1, 1)]
c = DailyCap(0.001, today=lambda: day[0])
assert c.is_open()
c.add(cost_usd(1000, 100))
print("spent after one call:", round(c.spent, 6), "open:", c.is_open())
assert not c.is_open(), "1000 input and 100 output tokens go over $0.001"
day[0] = date(2026, 1, 2)
assert c.is_open() and c.spent == 0, "a new day resets the total"
print("all checks passed")
