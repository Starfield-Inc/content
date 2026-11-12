import unittest
from pathlib import Path

from app.settings import load_env

ROOT = Path(__file__).resolve().parent.parent


class RepoSetupTests(unittest.TestCase):
    def test_env_example_lists_the_settings(self):
        names = load_env(ROOT / ".env.example")
        self.assertIn("TEAM_NAME", names)
        self.assertIn("API_KEY", names)

    def test_env_example_holds_no_real_key(self):
        self.assertEqual(load_env(ROOT / ".env.example")["API_KEY"], "paste-your-key-here")

    def test_missing_env_file_gives_empty_settings(self):
        self.assertEqual(load_env(ROOT / "no-such-file.env"), {})

    def test_gitignore_lists_env(self):
        lines = (ROOT / ".gitignore").read_text().splitlines()
        self.assertIn(".env", lines)


if __name__ == "__main__":
    unittest.main()
