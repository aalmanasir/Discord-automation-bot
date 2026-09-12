"""Fail-closed operator policy for the optional OpenClaw command."""

import os
import re


def openclaw_allowed(user_id: int, remote: str) -> bool:
    """Allow only configured Discord user IDs and one configured named remote."""
    raw = os.getenv("OPENCLAW_ALLOWED_USER_IDS", "")
    users = [value.strip() for value in raw.split(",")]
    if not users or any(not re.fullmatch(r"[1-9][0-9]{0,19}", value) for value in users):
        return False
    configured_remote = os.getenv("OPENCLAW_REMOTE", "origin")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", configured_remote):
        return False
    return str(user_id) in users and remote == configured_remote
