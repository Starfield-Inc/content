import unittest
from datetime import datetime, timezone

from filters import base_models, in_window, rule_any_base_model, rule_other_author_base


def model(name, tags=(), created="2026-11-01T00:00:00.000Z"):
    return {"id": name, "tags": list(tags), "createdAt": created}


class FilterTests(unittest.TestCase):
    def test_other_author_quantised_copy_is_dropped(self):
        m = model("unsloth/X-GGUF", ["base_model:quantized:mistralai/X"])
        self.assertTrue(rule_other_author_base(m, "unsloth"))

    def test_own_quantised_release_is_kept(self):
        m = model("Qwen/X-FP8", ["base_model:Qwen/X", "base_model:quantized:Qwen/X"])
        self.assertFalse(rule_other_author_base(m, "Qwen"))
        self.assertTrue(rule_any_base_model(m, "Qwen"))

    def test_model_without_base_tag_is_kept(self):
        self.assertFalse(rule_other_author_base(model("google/Y"), "google"))

    def test_short_and_long_tag_forms_are_read(self):
        m = model("a/b", ["base_model:o/n", "base_model:finetune:o/n"])
        self.assertEqual(base_models(m), [("", "o/n"), ("finetune", "o/n")])

    def test_date_window(self):
        now = datetime(2026, 11, 10, tzinfo=timezone.utc)
        self.assertTrue(in_window(model("a/b", created="2026-11-01T00:00:00.000Z"), 10, now))
        self.assertFalse(in_window(model("a/b", created="2026-10-01T00:00:00.000Z"), 10, now))


if __name__ == "__main__":
    unittest.main()
