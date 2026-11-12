"""Two guards for an LLM endpoint: a per-user request limit and a daily cost cap.

Both keep their counters in memory. They are lost when the process restarts.
"""
import threading
import time
from collections import defaultdict, deque
from datetime import datetime, timezone

# ASSUMPTION: example prices in US dollars per million tokens, chosen for this tutorial.
# They are not published facts. Check the current price list for your model and change them.
EXAMPLE_INPUT_PRICE_PER_MILLION = 1.00
EXAMPLE_OUTPUT_PRICE_PER_MILLION = 5.00


def cost_usd(input_tokens, output_tokens):
    """Cost of one call from the token counts the API returned, at the example prices above."""
    return (input_tokens * EXAMPLE_INPUT_PRICE_PER_MILLION + output_tokens * EXAMPLE_OUTPUT_PRICE_PER_MILLION) / 1_000_000


class RateLimiter:
    """Sliding window: at most `limit` requests per user in the last `window` seconds."""

    def __init__(self, limit, window, clock=time.monotonic):
        self.limit, self.window, self.clock = limit, window, clock
        self.hits = defaultdict(deque)
        self.lock = threading.Lock()

    def allow(self, user):
        """Return 0 if the request is allowed (and count it), else seconds to wait."""
        with self.lock:
            now = self.clock()
            q = self.hits[user]
            while q and now - q[0] >= self.window:
                q.popleft()
            if len(q) >= self.limit:
                return max(1, int(self.window - (now - q[0])) + 1)
            q.append(now)
            return 0


class DailyCap:
    """Total spend per UTC day. The total resets when the date changes."""

    def __init__(self, cap_usd, today=lambda: datetime.now(timezone.utc).date()):
        self.cap_usd, self.today = cap_usd, today
        self.day, self.spent, self.calls = today(), 0.0, 0
        self.lock = threading.Lock()

    def _roll(self):
        if self.today() != self.day:
            self.day, self.spent, self.calls = self.today(), 0.0, 0

    def is_open(self):
        with self.lock:
            self._roll()
            return self.spent < self.cap_usd

    def add(self, amount):
        with self.lock:
            self._roll()
            self.spent += amount
            self.calls += 1
            return self.spent
