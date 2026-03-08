"""Unit tests for bot response formatting helpers."""

import sys
import os
import unittest

# Allow importing from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from backend.utils.response_helpers import build_mismatch_message


class TestBuildMismatchMessage(unittest.TestCase):
    """Tests for the build_mismatch_message helper."""

    def test_text_mismatch_no_filename(self):
        msg = build_mismatch_message("abc123", "def456")
        self.assertIn("❌", msg)
        self.assertIn("abc123", msg)
        self.assertIn("def456", msg)
        self.assertIn("The SHA256 hash of your text", msg)

    def test_file_mismatch_includes_filename(self):
        msg = build_mismatch_message("abc123", "def456", filename="report.pdf")
        self.assertIn("❌", msg)
        self.assertIn("abc123", msg)
        self.assertIn("def456", msg)
        self.assertIn("report.pdf", msg)
        self.assertNotIn("your text", msg)

    def test_computed_and_expected_labels_present(self):
        msg = build_mismatch_message("aaa", "bbb")
        self.assertIn("Computed:", msg)
        self.assertIn("Expected:", msg)

    def test_empty_filename_treated_as_text(self):
        msg_no_file = build_mismatch_message("aaa", "bbb", filename="")
        msg_default = build_mismatch_message("aaa", "bbb")
        self.assertEqual(msg_no_file, msg_default)


if __name__ == "__main__":
    unittest.main()
