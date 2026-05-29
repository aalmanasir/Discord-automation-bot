"""Unit tests for bot helper functions."""

import sys
import os
import unittest

# Allow importing from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from bot import _format_verify_result

DIGEST = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
WRONG = "0" * 64


class TestFormatVerifyResultText(unittest.TestCase):
    """Tests for _format_verify_result without a filename (text mode)."""

    def test_match(self):
        result = _format_verify_result(DIGEST, DIGEST, match=True)
        self.assertIn("✅", result)
        self.assertIn("Match", result)
        self.assertIn(DIGEST, result)

    def test_mismatch(self):
        result = _format_verify_result(DIGEST, WRONG, match=False)
        self.assertIn("❌", result)
        self.assertIn("Mismatch", result)
        self.assertIn(DIGEST, result)
        self.assertIn(WRONG, result)

    def test_mismatch_normalizes_expected(self):
        # A hash with uppercase letters that doesn't match DIGEST
        upper_hash = "ABCDEF" + "0" * 58
        result = _format_verify_result(DIGEST, upper_hash, match=False)
        # Displayed expected value must be lowercased
        self.assertIn(upper_hash.lower(), result)
        self.assertNotIn(upper_hash, result)

    def test_mismatch_strips_whitespace_in_display(self):
        padded = "  " + WRONG + "  "
        result = _format_verify_result(DIGEST, padded, match=False)
        self.assertIn(WRONG, result)
        self.assertNotIn("  " + WRONG, result)


class TestFormatVerifyResultFile(unittest.TestCase):
    """Tests for _format_verify_result with a filename (file mode)."""

    def test_match_includes_filename(self):
        result = _format_verify_result(DIGEST, DIGEST, match=True, filename="test.bin")
        self.assertIn("✅", result)
        self.assertIn("test.bin", result)
        self.assertIn(DIGEST, result)

    def test_mismatch_includes_filename(self):
        result = _format_verify_result(DIGEST, WRONG, match=False, filename="test.bin")
        self.assertIn("❌", result)
        self.assertIn("test.bin", result)
        self.assertIn(DIGEST, result)
        self.assertIn(WRONG, result)

    def test_mismatch_normalizes_expected_with_filename(self):
        upper_hash = "ABCDEF" + "0" * 58
        result = _format_verify_result(DIGEST, upper_hash, match=False, filename="f.bin")
        self.assertIn(upper_hash.lower(), result)
        self.assertNotIn(upper_hash, result)


if __name__ == "__main__":
    unittest.main()
