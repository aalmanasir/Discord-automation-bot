"""Unit tests for git_helpers used by the OpenClaw Discord command."""

import inspect
import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Allow importing from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from git_helpers import GitError, git_push


def _make_completed_process(returncode: int, stdout: str = "", stderr: str = ""):
    mock = MagicMock()
    mock.returncode = returncode
    mock.stdout = stdout
    mock.stderr = stderr
    return mock


class TestGitPushSuccess(unittest.TestCase):
    """git_push returns combined output when git exits with code 0."""

    @patch("git_helpers.subprocess.run")
    def test_default_remote_and_branch(self, mock_run):
        mock_run.return_value = _make_completed_process(0, stdout="Everything up-to-date")
        result = git_push("/some/repo")
        mock_run.assert_called_once_with(
            ["git", "-C", "/some/repo", "push", "origin"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertEqual(result, "Everything up-to-date")

    @patch("git_helpers.subprocess.run")
    def test_custom_remote(self, mock_run):
        mock_run.return_value = _make_completed_process(0, stdout="Pushed")
        git_push("/repo", remote="upstream")
        cmd = mock_run.call_args[0][0]
        self.assertIn("upstream", cmd)
        self.assertNotIn("origin", cmd)

    @patch("git_helpers.subprocess.run")
    def test_branch_appended_when_provided(self, mock_run):
        mock_run.return_value = _make_completed_process(0, stderr="branch pushed")
        result = git_push("/repo", branch="main")
        cmd = mock_run.call_args[0][0]
        self.assertEqual(cmd[-1], "main")
        self.assertEqual(result, "branch pushed")

    @patch("git_helpers.subprocess.run")
    def test_no_branch_arg_when_none(self, mock_run):
        mock_run.return_value = _make_completed_process(0)
        git_push("/repo", branch=None)
        cmd = mock_run.call_args[0][0]
        # Should end after the remote name — no extra branch argument
        self.assertEqual(cmd, ["git", "-C", "/repo", "push", "origin"])

    @patch("git_helpers.subprocess.run")
    def test_stdout_and_stderr_combined(self, mock_run):
        mock_run.return_value = _make_completed_process(
            0, stdout="To github.com:user/repo\n", stderr="remote: Resolving\n"
        )
        result = git_push("/repo")
        self.assertIn("To github.com", result)
        self.assertIn("remote: Resolving", result)

    @patch("git_helpers.subprocess.run")
    def test_empty_output_returns_empty_string(self, mock_run):
        mock_run.return_value = _make_completed_process(0)
        result = git_push("/repo")
        self.assertEqual(result, "")


class TestGitPushFailure(unittest.TestCase):
    """git_push raises GitError when git exits with a non-zero code."""

    @patch("git_helpers.subprocess.run")
    def test_raises_git_error_on_nonzero(self, mock_run):
        mock_run.return_value = _make_completed_process(
            1, stderr="fatal: repository not found"
        )
        with self.assertRaises(GitError) as ctx:
            git_push("/repo")
        self.assertIn("repository not found", str(ctx.exception))

    @patch("git_helpers.subprocess.run")
    def test_error_message_contains_exit_code_when_no_output(self, mock_run):
        mock_run.return_value = _make_completed_process(128)
        with self.assertRaises(GitError) as ctx:
            git_push("/repo")
        self.assertIn("128", str(ctx.exception))

    @patch("git_helpers.subprocess.run")
    def test_git_error_is_exception(self, mock_run):
        mock_run.return_value = _make_completed_process(1, stderr="error")
        with self.assertRaises(Exception):
            git_push("/repo")


class TestGitPushNoPATAccepted(unittest.TestCase):
    """Confirm git_push has no parameter that could accept a PAT."""

    def test_signature_has_no_pat_parameter(self):
        sig = inspect.signature(git_push)
        param_names = list(sig.parameters.keys())
        for forbidden in ("pat", "token", "password", "credential", "secret"):
            self.assertNotIn(
                forbidden,
                param_names,
                msg=f"git_push must not accept a '{forbidden}' parameter",
            )

    def test_only_accepted_parameters(self):
        sig = inspect.signature(git_push)
        self.assertEqual(
            list(sig.parameters.keys()), ["repo_path", "remote", "branch", "timeout"]
        )


class TestGitPushValidation(unittest.TestCase):
    """git_push rejects unsafe remote and branch values."""

    def test_valid_remote_name(self):
        with patch("git_helpers.subprocess.run") as mock_run:
            mock_run.return_value = _make_completed_process(0)
            git_push("/repo", remote="upstream")  # should not raise

    def test_valid_remote_url_https(self):
        with patch("git_helpers.subprocess.run") as mock_run:
            mock_run.return_value = _make_completed_process(0)
            git_push("/repo", remote="https://github.com/user/repo.git")

    def test_valid_remote_url_ssh(self):
        with patch("git_helpers.subprocess.run") as mock_run:
            mock_run.return_value = _make_completed_process(0)
            git_push("/repo", remote="git@github.com:user/repo.git")

    def test_invalid_remote_raises_value_error(self):
        with self.assertRaises(ValueError):
            git_push("/repo", remote="; rm -rf /")

    def test_invalid_remote_with_shell_metachar(self):
        with self.assertRaises(ValueError):
            git_push("/repo", remote="origin && evil")

    def test_valid_branch(self):
        with patch("git_helpers.subprocess.run") as mock_run:
            mock_run.return_value = _make_completed_process(0)
            git_push("/repo", branch="feature/my-branch")  # should not raise

    def test_invalid_branch_raises_value_error(self):
        with self.assertRaises(ValueError):
            git_push("/repo", branch="main; evil")

    def test_invalid_branch_with_spaces(self):
        with self.assertRaises(ValueError):
            git_push("/repo", branch="bad branch")


class TestGitPushTimeout(unittest.TestCase):
    """git_push raises TimeoutError when the subprocess times out."""

    @patch("git_helpers.subprocess.run")
    def test_timeout_raises_timeout_error(self, mock_run):
        import subprocess as sp
        mock_run.side_effect = sp.TimeoutExpired(cmd=["git"], timeout=60)
        with self.assertRaises(TimeoutError) as ctx:
            git_push("/repo")
        self.assertIn("60", str(ctx.exception))

    @patch("git_helpers.subprocess.run")
    def test_custom_timeout_passed_to_subprocess(self, mock_run):
        mock_run.return_value = _make_completed_process(0)
        git_push("/repo", timeout=30)
        _, kwargs = mock_run.call_args
        self.assertEqual(kwargs["timeout"], 30)


if __name__ == "__main__":
    unittest.main()
