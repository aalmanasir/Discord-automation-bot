"""Bot response formatting helpers shared across command handlers."""


def build_mismatch_message(computed: str, expected: str, filename: str = "") -> str:
    """Return a formatted mismatch message for hash-verification commands.

    Args:
        computed: The SHA256 hex-digest that was actually computed.
        expected: The already-normalised expected hex-digest supplied by the user.
        filename: Optional filename shown when hashing a file attachment.

    Returns:
        A Discord-ready mismatch message string.
    """
    subject = f"SHA256 of `{filename}`" if filename else "The SHA256 hash of your text"
    return (
        f"❌ **Mismatch!** {subject} does not match the expected hash.\n"
        f"Computed: `{computed}`\n"
        f"Expected: `{expected}`"
    )
