"""SHA256 service — business logic for hashing and verification commands."""

import logging

from backend.utils.sha256_helpers import (
    compute_sha256_bytes,
    compute_sha256_text,
    verify_sha256,
)

logger = logging.getLogger(__name__)


def hash_text(text: str) -> str:
    """Compute and return the SHA256 hex-digest of *text*.

    Args:
        text: The text string to hash.

    Returns:
        A 64-character lowercase hex string.
    """
    digest = compute_sha256_text(text)
    logger.debug("Computed SHA256 for text input (length=%d)", len(text))
    return digest


def hash_bytes(data: bytes) -> str:
    """Compute and return the SHA256 hex-digest of raw *data*.

    Args:
        data: The raw bytes to hash.

    Returns:
        A 64-character lowercase hex string.
    """
    digest = compute_sha256_bytes(data)
    logger.debug("Computed SHA256 for bytes input (length=%d)", len(data))
    return digest


def _verify_and_log(digest: str, expected_hash: str, source: str) -> tuple[str, bool]:
    """Verify *digest* against *expected_hash* and log the result.

    Args:
        digest: The already-computed SHA256 hex-digest.
        expected_hash: The expected SHA256 hex-digest.
        source: A label used in the log message (e.g. ``"text"`` or ``"bytes"``).

    Returns:
        A tuple of (digest, match) where *match* is True when the digests
        are equal (case-insensitive, whitespace-stripped).
    """
    match = verify_sha256(digest, expected_hash)
    logger.debug(
        "SHA256 %s verification: match=%s, expected=%s",
        source,
        match,
        expected_hash.strip()[:16] + "…",
    )
    return digest, match


def verify_text_hash(text: str, expected_hash: str) -> tuple[str, bool]:
    """Hash *text* and compare against *expected_hash*.

    Args:
        text: The text string to hash.
        expected_hash: The expected SHA256 hex-digest.

    Returns:
        A tuple of (computed_digest, match) where *match* is True when they
        are equal (case-insensitive, whitespace-stripped).
    """
    return _verify_and_log(compute_sha256_text(text), expected_hash, "text")


def verify_bytes_hash(data: bytes, expected_hash: str) -> tuple[str, bool]:
    """Hash *data* and compare against *expected_hash*.

    Args:
        data: The raw bytes to hash.
        expected_hash: The expected SHA256 hex-digest.

    Returns:
        A tuple of (computed_digest, match) where *match* is True when they
        are equal (case-insensitive, whitespace-stripped).
    """
    return _verify_and_log(compute_sha256_bytes(data), expected_hash, "bytes")
