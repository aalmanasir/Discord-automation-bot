"""SHA256 helper utilities shared by the bot commands and tests."""

import hashlib


def compute_sha256_text(text: str) -> str:
    """Return the SHA256 hex-digest of *text* encoded as UTF-8."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def compute_sha256_bytes(data: bytes) -> str:
    """Return the SHA256 hex-digest of raw *data*."""
    return hashlib.sha256(data).hexdigest()


def verify_sha256(digest: str, expected_hash: str) -> bool:
    """Return True when *digest* equals *expected_hash* (case-insensitive, stripped)."""
    return digest == expected_hash.strip().lower()
