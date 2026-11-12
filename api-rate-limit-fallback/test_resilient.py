import logging
import unittest

import anthropic
from anthropic import Anthropic

from resilient import ask, backoff_delay
from standin import StandIn

SAVED = "saved answer text"
logging.getLogger("resilient").addHandler(logging.NullHandler())  # keep test output quiet


def run(stand_in, **options):
    """Call ask() with a client that does not retry, and sleeps that are recorded, not slept."""
    sleeps = []
    client = Anthropic(base_url=stand_in.base_url, api_key="stand-in-key", max_retries=0)
    options.setdefault("rand", lambda: 1.0)
    answer = ask(client, "hello", SAVED, sleep=sleeps.append, **options)
    return answer, sleeps


class RetryTests(unittest.TestCase):
    def test_no_failure_means_one_call_and_no_sleep(self):
        with StandIn(fail=0) as stand_in:
            answer, sleeps = run(stand_in)
        self.assertEqual((answer.source, answer.attempts, sleeps), ("live", 1, []))
        self.assertEqual(len(stand_in.calls), 1)

    def test_429_with_retry_after_waits_that_long_plus_jitter(self):
        with StandIn(fail=2, status=429, retry_after=3) as stand_in:
            answer, sleeps = run(stand_in, base=0.5)
        self.assertEqual((answer.source, answer.attempts), ("live", 3))
        self.assertEqual(sleeps, [3.5, 3.5])
        self.assertEqual(len(stand_in.calls), 3)

    def test_529_without_header_backs_off_exponentially_to_the_cap(self):
        with StandIn(fail=3, status=529, retry_after=None) as stand_in:
            answer, sleeps = run(stand_in, max_attempts=5, base=0.5, cap=1.5)
        self.assertEqual(answer.source, "live")
        self.assertEqual(sleeps, [0.5, 1.0, 1.5])

    def test_each_retry_is_logged(self):
        with StandIn(fail=2, status=429, retry_after=1) as stand_in:
            with self.assertLogs("resilient", level="WARNING") as logs:
                run(stand_in)
        self.assertEqual(len(logs.records), 2)
        self.assertIn("retry 1 of 3: RateLimitError (status 429)", logs.output[0])
        self.assertIn("retry 2 of 3", logs.output[1])

    def test_jitter_keeps_the_wait_between_zero_and_the_ceiling(self):
        error = anthropic.APIConnectionError(request=None)
        self.assertEqual(backoff_delay(3, error, base=0.5, rand=lambda: 0.0), 0.0)
        self.assertEqual(backoff_delay(3, error, base=0.5, rand=lambda: 1.0), 2.0)


class FallbackTests(unittest.TestCase):
    def test_saved_answer_after_the_last_attempt(self):
        with StandIn(fail=99, status=529, retry_after=None) as stand_in:
            answer, sleeps = run(stand_in, max_attempts=3)
        self.assertEqual((answer.text, answer.source, answer.attempts), (SAVED, "saved", 3))
        self.assertEqual(len(sleeps), 2)
        self.assertEqual(len(stand_in.calls), 3)

    def test_long_retry_after_goes_straight_to_the_saved_answer(self):
        with StandIn(fail=99, status=429, retry_after=60) as stand_in:
            answer, sleeps = run(stand_in, max_wait=10)
        self.assertEqual((answer.source, sleeps), ("saved", []))
        self.assertEqual(len(stand_in.calls), 1)

    def test_a_bad_key_is_raised_not_hidden_by_the_fallback(self):
        with StandIn(fail=99, status=401, retry_after=None) as stand_in:
            with self.assertRaises(anthropic.AuthenticationError):
                run(stand_in)
        self.assertEqual(len(stand_in.calls), 1)


if __name__ == "__main__":
    unittest.main()
