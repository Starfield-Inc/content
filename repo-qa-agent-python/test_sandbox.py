import os
import tempfile
import unittest
from pathlib import Path

from repo_tools import RepoTools


class SandboxTests(unittest.TestCase):
    def setUp(self):
        self.tools = RepoTools("sample_repo")

    def test_reads_inside(self):
        self.assertIn("shelf", self.tools.run("read_file", {"path": "README.md"}))

    def test_blocks_parent_folder(self):
        self.assertTrue(self.tools.run("read_file", {"path": "../private/notes.txt"}).startswith("refused"))

    def test_blocks_absolute_path(self):
        self.assertTrue(self.tools.run("read_file", {"path": "/etc/hosts"}).startswith("refused"))

    def test_blocks_symlink_out(self):
        outside = Path(tempfile.mkdtemp()) / "secret.txt"
        outside.write_text("outside")
        repo = Path(tempfile.mkdtemp())
        os.symlink(outside, repo / "link.txt")
        self.assertTrue(RepoTools(repo).run("read_file", {"path": "link.txt"}).startswith("refused"))
        self.assertNotIn("link.txt", RepoTools(repo).run("list_files", {}))

    def test_prefix_trick(self):
        base = Path(tempfile.mkdtemp())
        (base / "repo").mkdir()
        (base / "repo-private").mkdir()
        (base / "repo-private" / "x.txt").write_text("x")
        result = RepoTools(base / "repo").run("read_file", {"path": "../repo-private/x.txt"})
        self.assertTrue(result.startswith("refused"))


if __name__ == "__main__":
    unittest.main()
