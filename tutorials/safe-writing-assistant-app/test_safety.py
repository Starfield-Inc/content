"""Checks that need no key and no network: python -m unittest -v test_safety"""
import unittest

from safety import MAX_DRAFT_CHARS, Rejected, check_length


class LengthTests(unittest.TestCase):
    def test_normal_draft_passes_and_is_trimmed(self):
        self.assertEqual(check_length("  Hello there.  "), "Hello there.")

    def test_empty_is_rejected(self):
        for value in ("", "   ", None):
            with self.assertRaises(Rejected):
                check_length(value)

    def test_limit_is_inclusive(self):
        self.assertEqual(len(check_length("a" * MAX_DRAFT_CHARS)), MAX_DRAFT_CHARS)
        with self.assertRaises(Rejected) as ctx:
            check_length("a" * (MAX_DRAFT_CHARS + 1))
        self.assertIn(str(MAX_DRAFT_CHARS + 1), str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
