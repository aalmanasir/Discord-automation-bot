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


def hash_bytes(raw_bytes: bytes) -> str:
    """Compute and return the SHA256 hex-digest of raw *raw_bytes*.

    Args:
        raw_bytes: The raw bytes to hash.

    Returns:
        A 64-character lowercase hex string.
    """
    digest = compute_sha256_bytes(raw_bytes)
    logger.debug("Computed SHA256 for bytes input (length=%d)", len(raw_bytes))
    return digest


def verify_text_hash(text: str, expected_hash: str) -> tuple[str, bool]:
    """Hash *text* and compare against *expected_hash*.

    Args:
        text: The text string to hash.
        expected_hash: The expected SHA256 hex-digest.

    Returns:
        A tuple of (computed_digest, match) where *match* is True when they
        are equal (case-insensitive, whitespace-stripped).
    """
    digest = compute_sha256_text(text)
    match = verify_sha256(digest, expected_hash)
    logger.debug(
        "SHA256 text verification: match=%s, expected=%s",
        match,
        expected_hash.strip()[:16] + "…",
    )
    return digest, match


def verify_bytes_hash(raw_bytes: bytes, expected_hash: str) -> tuple[str, bool]:
    """Hash *raw_bytes* and compare against *expected_hash*.

    Args:
        raw_bytes: The raw bytes to hash.
        expected_hash: The expected SHA256 hex-digest.

    Returns:
        A tuple of (computed_digest, match) where *match* is True when they
        are equal (case-insensitive, whitespace-stripped).
    """
    digest = compute_sha256_bytes(raw_bytes)
    match = verify_sha256(digest, expected_hash)
    logger.debug(
        "SHA256 bytes verification: match=%s, expected=%s",
        match,
        expected_hash.strip()[:16] + "…",
    )
    return digest, match
