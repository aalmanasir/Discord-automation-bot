<<<<<<< HEAD
"""Backward-compatible re-export shim for sha256_helpers.

New code should import from backend.utils.sha256_helpers directly.
=======
"""SHA256 helper utilities — re-exported from backend.utils for compatibility.

New code should import directly from ``backend.utils.sha256_helpers``.
>>>>>>> origin/main
"""

from backend.utils.sha256_helpers import (  # noqa: F401
    compute_sha256_bytes,
    compute_sha256_text,
    verify_sha256,
)
