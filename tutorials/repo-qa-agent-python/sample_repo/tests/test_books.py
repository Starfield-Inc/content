import tempfile
import unittest
from pathlib import Path

from shelf.books import add_book, mark_read


class BookTests(unittest.TestCase):
    def test_add_and_mark_read(self):
        path = Path(tempfile.mkdtemp()) / "books.json"
        add_book("Dune", "Frank Herbert", path)
        self.assertTrue(mark_read("Dune", path))
        self.assertFalse(mark_read("Missing", path))

    def test_empty_title_rejected(self):
        with self.assertRaises(ValueError):
            add_book("  ", "Nobody", Path("unused.json"))
