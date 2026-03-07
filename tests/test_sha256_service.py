"""Unit tests for the SHA256 service layer."""

import sys
import os
import unittest

# Allow importing from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from backend.services.sha256_service import (
    hash_bytes,
    hash_text,
    verify_bytes_hash,
    verify_text_hash,
)


class TestHashText(unittest.TestCase):
    """Tests for the hash_text service function."""

    def test_known_value(self):
        expected = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        self.assertEqual(hash_text("hello"), expected)

    def test_empty_string(self):
        expected = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        self.assertEqual(hash_text(""), expected)

    def test_returns_lowercase_hex(self):
        digest = hash_text("test")
        self.assertEqual(digest, digest.lower())
        self.assertEqual(len(digest), 64)


class TestHashBytes(unittest.TestCase):
    """Tests for the hash_bytes service function."""

    def test_known_bytes(self):
        expected = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        self.assertEqual(hash_bytes(b"hello"), expected)

    def test_empty_bytes(self):
        expected = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        self.assertEqual(hash_bytes(b""), expected)

    def test_consistency_with_hash_text(self):
        text = "discord bot"
        self.assertEqual(hash_text(text), hash_bytes(text.encode("utf-8")))


class TestVerifyTextHash(unittest.TestCase):
    """Tests for the verify_text_hash service function."""

    def test_match(self):
        digest_direct = hash_text("hello")
        digest, match = verify_text_hash("hello", digest_direct)
        self.assertTrue(match)
        self.assertEqual(digest, digest_direct)

    def test_mismatch(self):
        expected_wrong = hash_text("world")
        _, match = verify_text_hash("hello", expected_wrong)
        self.assertFalse(match)

    def test_case_insensitive(self):
        digest = hash_text("hello")
        _, match = verify_text_hash("hello", digest.upper())
        self.assertTrue(match)

    def test_strips_whitespace(self):
        digest = hash_text("hello")
        _, match = verify_text_hash("hello", "  " + digest + "  ")
        self.assertTrue(match)


class TestVerifyBytesHash(unittest.TestCase):
    """Tests for the verify_bytes_hash service function."""

    def test_match(self):
        data = b"hello"
        expected = hash_bytes(data)
        digest, match = verify_bytes_hash(data, expected)
        self.assertTrue(match)
        self.assertEqual(digest, expected)

    def test_mismatch(self):
        _, match = verify_bytes_hash(b"hello", hash_bytes(b"world"))
        self.assertFalse(match)

    def test_case_insensitive(self):
        data = b"hello"
        digest = hash_bytes(data)
        _, match = verify_bytes_hash(data, digest.upper())
        self.assertTrue(match)


if __name__ == "__main__":
    unittest.main()
