"""SHA256 helper utilities shared by the bot commands and tests."""

import hashlib
import hmac


def normalize_hash(expected: str) -> str:
    """Return *expected* stripped of surrounding whitespace and lowercased."""
    return expected.strip().lower()


def compute_sha256_text(text: str) -> str:
    """Return the SHA256 hex-digest of *text* encoded as UTF-8."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def compute_sha256_bytes(data: bytes) -> str:
    """Return the SHA256 hex-digest of raw *data*."""
    return hashlib.sha256(data).hexdigest()


def verify_sha256(digest: str, expected: str) -> bool:
    """Return True when *digest* equals *expected* (case-insensitive, stripped).

    Uses hmac.compare_digest for a timing-safe comparison that resists
    timing-based side-channel attacks.
    """
    return hmac.compare_digest(digest, normalize_hash(expected))
