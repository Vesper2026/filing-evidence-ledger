import unittest
from filing_evidence import review, render


class LedgerTests(unittest.TestCase):
    def row(self, **updates):
        row = dict(id="E01", question="Revenue?", title="Synthetic", source_url="https://eqvero.com/", location="p12", quote="收入 12.00", value="12.00", unit="million", period="FY2025")
        row.update(updates)
        return row

    def test_preserves_evidence_and_precision(self):
        result = review({"evidence": [self.row()]})
        self.assertEqual(result["items"][0]["evidence"]["value"], "12.00")
        self.assertEqual(result["items_needing_attention"], 0)
        self.assertIn("收入 12.00", render(result))

    def test_missing_period_and_quote(self):
        result = review({"evidence": [self.row(period="", quote="")]})
        self.assertEqual(set(result["items"][0]["checks"]), {"missing:period", "missing:quote"})

    def test_duplicate_ids_are_not_overwritten(self):
        result = review({"evidence": [self.row(), self.row()]})
        self.assertEqual(len(result["items"]), 2)
        self.assertTrue(all("duplicate:id" in item["checks"] for item in result["items"]))

    def test_status_does_not_mean_verification(self):
        result = review({"evidence": [self.row(status="reviewed")]})
        self.assertIn("NOT been verified", result["notice"])
        self.assertEqual(result["items"][0]["review_status"], "reviewed")

    def test_render_escapes_markup_and_numeric_zero(self):
        result = review({"evidence": [self.row(quote="<script>|[bad]", value="0")]})
        self.assertIn("&lt;script&gt;\\|\\[bad\\]", render(result))
        self.assertEqual(result["items_needing_attention"], 0)

    def test_invalid_shape_and_non_string_value(self):
        with self.assertRaises(ValueError):
            review([])
        result = review({"evidence": [self.row(value=0)]})
        self.assertIn("value:use_string_to_preserve_original_precision", result["items"][0]["checks"])


if __name__ == "__main__":
    unittest.main()
