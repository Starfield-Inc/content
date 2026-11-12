import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dedupe import group

ITEMS = [
    {"source": "Feed A", "title": "Meta launches Muse Ember, a small AI model built for the real world"},
    {"source": "Feed B", "title": "Meta introduces Muse Ember to power cost-efficient AI agents"},
    {"source": "Feed A", "title": "Acme releases Atlas 2.0 with a longer context window"},
    {"source": "Feed B", "title": "Acme releases Atlas 1.0 with a longer context window"},
    {"source": "Feed C", "title": "A weekly reading list on open models"},
]


class DedupeTest(unittest.TestCase):
    def setUp(self):
        self.groups = group(ITEMS)
        self.titles = [{i["title"] for i in g} for g in self.groups]

    def test_same_story_from_two_feeds_is_grouped(self):
        self.assertTrue(any(len(t) == 2 and ITEMS[0]["title"] in t and ITEMS[1]["title"] in t for t in self.titles))

    def test_different_version_numbers_stay_apart(self):
        for t in self.titles:
            self.assertFalse(ITEMS[2]["title"] in t and ITEMS[3]["title"] in t)

    def test_unrelated_item_stays_alone(self):
        self.assertIn({ITEMS[4]["title"]}, self.titles)


if __name__ == "__main__":
    unittest.main(verbosity=2)
