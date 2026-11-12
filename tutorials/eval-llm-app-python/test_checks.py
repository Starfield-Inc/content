"""Tests for the checker itself, with fixed replies and no API call."""
import unittest

from run_eval import check


class CheckTests(unittest.TestCase):
    def test_passes_when_any_option_is_present(self):
        case = {"must_include": [["30 days", "30-day"]]}
        self.assertEqual(check(case, "Returns within 30 days."), [])

    def test_fails_when_nothing_matches(self):
        case = {"must_include": [["30 days", "30-day"]]}
        self.assertEqual(len(check(case, "Returns are fine.")), 1)

    def test_forbidden_text_fails(self):
        case = {"must_not_include": ["i promise"]}
        self.assertEqual(len(check(case, "I promise a refund.")), 1)

    def test_word_limit(self):
        self.assertEqual(len(check({"max_words": 3}, "one two three four")), 1)

    def test_empty_reply_fails(self):
        self.assertEqual(check({"must_include": [["x"]]}, ""), ["empty reply"])


if __name__ == "__main__":
    unittest.main()
