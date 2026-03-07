"""Git helper utilities for the OpenClaw push command.

Authentication relies entirely on the environment's SSH keys or system
credential manager.  No PAT is ever accepted as a function argument so
credentials cannot accidentally be leaked through Discord chat.
"""

import re
import subprocess
from typing import Optional

# Matches a plain remote name (alphanumeric, hyphens, underscores, dots)
_REMOTE_NAME_RE = re.compile(r"^[A-Za-z0-9_.\-]+$")
# Matches a URL-style remote (https, http, git, ssh, or SCP-style git@host:path)
_REMOTE_URL_RE = re.compile(
    r"^(https?://|git://|ssh://|git@)[A-Za-z0-9._/:\-@~%?&=#]+$"
)

# Matches a valid git ref / branch name component.
# Allows hierarchical refs such as "feature/my-branch".
_BRANCH_RE = re.compile(r"^[A-Za-z0-9_.\-/]+$")

# Default push timeout in seconds; generous enough for large repos over a
# slow connection but still prevents the bot from hanging indefinitely.
_DEFAULT_TIMEOUT = 60


class GitError(Exception):
    """Raised when a git operation exits with a non-zero status."""


def _validate_remote(remote: str) -> None:
    """Raise ``ValueError`` if *remote* is not a safe remote name or URL."""
    if not (_REMOTE_NAME_RE.match(remote) or _REMOTE_URL_RE.match(remote)):
        raise ValueError(
            f"Invalid remote '{remote}': must be a plain remote name or a "
            "git/ssh/https URL."
        )


def _validate_branch(branch: str) -> None:
    """Raise ``ValueError`` if *branch* is not a safe git ref name."""
    if not _BRANCH_RE.match(branch):
        raise ValueError(
            f"Invalid branch '{branch}': must contain only alphanumeric "
            "characters, hyphens, underscores, dots, or forward slashes."
        )


def git_push(
    repo_path: str,
    remote: str = "origin",
    branch: Optional[str] = None,
    timeout: int = _DEFAULT_TIMEOUT,
) -> str:
    """Push *repo_path* to *remote* using SSH / the system credential manager.

    Args:
        repo_path: Absolute or relative path to the local git repository.
        remote:    Remote name or URL (defaults to ``"origin"``).
        branch:    Branch ref to push.  When ``None`` git pushes the currently
                   checked-out branch according to the push.default config.
        timeout:   Seconds before the subprocess is killed (default: 60).

    Returns:
        Combined stdout + stderr output from git as a stripped string.

    Raises:
        ValueError:  If *remote* or *branch* contain unsafe characters.
        GitError:    If git exits with a non-zero status code.
        TimeoutError: If the git push does not complete within *timeout* seconds.
    """
    _validate_remote(remote)
    if branch:
        _validate_branch(branch)

    cmd = ["git", "-C", repo_path, "push", remote]
    if branch:
        cmd.append(branch)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise TimeoutError(
            f"git push timed out after {timeout} seconds"
        ) from exc

    output = (result.stdout + result.stderr).strip()

    if result.returncode != 0:
        raise GitError(
            output or f"git push failed with exit code {result.returncode}"
        )

    return output
