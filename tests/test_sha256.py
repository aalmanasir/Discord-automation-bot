"""Unit tests for SHA256 helper logic used by the Discord bot commands."""

import sys
import os
import unittest

# Allow importing from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from backend.utils.sha256_helpers import compute_sha256_bytes, compute_sha256_text, verify_sha256


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestComputeSha256Text(unittest.TestCase):
    """Tests for compute_sha256_text."""

    def test_known_value(self):
        # echo -n "hello" | sha256sum
        expected = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        self.assertEqual(compute_sha256_text("hello"), expected)

    def test_empty_string(self):
        # echo -n "" | sha256sum
        expected = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        self.assertEqual(compute_sha256_text(""), expected)

    def test_unicode_string(self):
        digest = compute_sha256_text("Héllo")
        self.assertEqual(len(digest), 64)
        self.assertTrue(all(c in "0123456789abcdef" for c in digest))

    def test_returns_lowercase_hex(self):
        digest = compute_sha256_text("test")
        self.assertEqual(digest, digest.lower())


class TestComputeSha256Bytes(unittest.TestCase):
    """Tests for compute_sha256_bytes."""

    def test_known_bytes(self):
        expected = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        self.assertEqual(compute_sha256_bytes(b"hello"), expected)

    def test_empty_bytes(self):
        expected = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        self.assertEqual(compute_sha256_bytes(b""), expected)

    def test_consistency_with_text(self):
        text = "discord bot"
        self.assertEqual(
            compute_sha256_text(text),
            compute_sha256_bytes(text.encode("utf-8")),
        )


class TestVerifySha256(unittest.TestCase):
    """Tests for verify_sha256."""

    def test_match(self):
        digest = compute_sha256_text("hello")
        self.assertTrue(verify_sha256(digest, digest))

    def test_mismatch(self):
        digest = compute_sha256_text("hello")
        wrong = compute_sha256_text("world")
        self.assertFalse(verify_sha256(digest, wrong))

    def test_case_insensitive(self):
        digest = compute_sha256_text("hello")
        self.assertTrue(verify_sha256(digest, digest.upper()))

    def test_strips_whitespace(self):
        digest = compute_sha256_text("hello")
        self.assertTrue(verify_sha256(digest, "  " + digest + "  "))

    def test_empty_vs_empty(self):
        digest = compute_sha256_text("")
        self.assertTrue(verify_sha256(digest, digest))


if __name__ == "__main__":
    unittest.main()
