import unittest

from checklist import run_checklist, sentences

SAMPLE = """Example Licence v1.

You may use the Model for non-commercial research only. Companies with more than 700 million monthly
active users must ask us for a licence. You must keep this copyright notice. This agreement is governed by
the laws of Ruritania."""


class ChecklistTests(unittest.TestCase):
    def test_wrapped_lines_become_one_sentence(self):
        self.assertIn("Companies with more than 700 million monthly active users must ask us for a licence.", sentences(SAMPLE))

    def test_each_question_finds_its_line(self):
        result = run_checklist(SAMPLE)
        self.assertTrue(any("non-commercial" in line for line, _ in result["commercial"]))
        self.assertTrue(any("700 million" in line for line, _ in result["limits"]))
        self.assertTrue(any("copyright notice" in line for line, _ in result["naming"]))
        self.assertTrue(any("Ruritania" in line for line, _ in result["law"]))

    def test_silence_gives_no_hits(self):
        self.assertEqual(run_checklist(SAMPLE)["outputs"], [])


if __name__ == "__main__":
    unittest.main()
