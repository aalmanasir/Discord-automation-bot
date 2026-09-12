"""Verify the command enforces policy before invoking Git and withholds raw output."""

import os
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from bot import openclaw_command
from git_helpers import GitError


def interaction():
    return SimpleNamespace(user=SimpleNamespace(id=123), response=SimpleNamespace(
        defer=AsyncMock(), send_message=AsyncMock()), followup=SimpleNamespace(send=AsyncMock()))


class OpenClawCommandTests(unittest.IsolatedAsyncioTestCase):
    async def test_disabled_command_never_invokes_git(self):
        request = interaction()
        with patch.dict(os.environ, {}, clear=True), patch('bot.git_push') as push:
            await openclaw_command.callback(request)
        push.assert_not_called()
        request.response.defer.assert_not_awaited()
        self.assertTrue(request.response.send_message.await_args.kwargs['ephemeral'])

    async def test_wrong_remote_never_invokes_git(self):
        request = interaction()
        with patch.dict(os.environ, {'OPENCLAW_ALLOWED_USER_IDS': '123'}, clear=True), patch('bot.git_push') as push:
            await openclaw_command.callback(request, remote='https://example.com/repo')
        push.assert_not_called()

    async def test_success_does_not_return_git_output(self):
        request = interaction()
        with patch.dict(os.environ, {'OPENCLAW_ALLOWED_USER_IDS': '123'}, clear=True), patch('bot.git_push', return_value='private-host-details') as push:
            await openclaw_command.callback(request)
        push.assert_called_once()
        request.followup.send.assert_awaited_once_with('Repository push completed.', ephemeral=True)

    async def test_failure_does_not_return_git_output(self):
        request = interaction()
        with patch.dict(os.environ, {'OPENCLAW_ALLOWED_USER_IDS': '123'}, clear=True), patch('bot.git_push', side_effect=GitError('private-host-details')):
            await openclaw_command.callback(request)
        self.assertNotIn('private-host-details', str(request.followup.send.await_args))
        self.assertTrue(request.followup.send.await_args.kwargs['ephemeral'])
