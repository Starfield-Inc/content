"""Prompt tests. Each test sends one prompt and checks the answer by rule.

Run:  python -m unittest -v test_prompts
Test another set of prompts:  PROMPTS_MODULE=prompts_changed python -m unittest -v test_prompts
"""
import importlib, json, os, unittest

from llm import ask, get_client

PROMPTS = importlib.import_module(os.environ.get("PROMPTS_MODULE", "prompts")).PROMPTS
get_client()  # exits with a clear message when there is no key


def word_count(text):
    return len(text.split())


class PromptTests(unittest.TestCase):
    def test_capital(self):
        out = ask(PROMPTS["capital"])
        with self.subTest(check="names Canberra"):
            self.assertIn("canberra", out.lower(), f"got: {out!r}")
        with self.subTest(check="at most 3 words"):
            self.assertLessEqual(word_count(out), 3, f"got: {out!r}")

    def test_json(self):
        out = ask(PROMPTS["json"])
        try:
            data = json.loads(out)
        except json.JSONDecodeError:
            self.fail(f"not valid JSON, got: {out!r}")
        with self.subTest(check="symbol is Au"):
            self.assertEqual(data.get("symbol"), "Au", f"got: {out!r}")
        with self.subTest(check="number is 79"):
            self.assertEqual(data.get("number"), 79, f"got: {out!r}")

    def test_list(self):
        out = ask(PROMPTS["list"])
        lines = [line for line in out.splitlines() if line.strip()]
        with self.subTest(check="three lines"):
            self.assertEqual(len(lines), 3, f"got: {out!r}")
        for colour in ("red", "green", "blue"):
            with self.subTest(check=f"mentions {colour}"):
                self.assertIn(colour, out.lower(), f"got: {out!r}")

    def test_summary(self):
        out = ask(PROMPTS["summary"])
        with self.subTest(check="under 20 words"):
            self.assertLess(word_count(out), 20, f"{word_count(out)} words")
        with self.subTest(check="mentions sunlight or light"):
            self.assertIn("light", out.lower(), f"got: {out!r}")
        with self.subTest(check="mentions sugar or glucose"):
            self.assertTrue(any(w in out.lower() for w in ("sugar", "glucose")), f"got: {out!r}")

    def test_minutes(self):
        out = ask(PROMPTS["minutes"])
        self.assertEqual(out.strip().rstrip("."), "180", f"got: {out!r}")


if __name__ == "__main__":
    unittest.main()
