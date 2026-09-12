"""Operator access policy tests without a Discord connection."""

import os
import unittest
from unittest.mock import patch

from backend.config.openclaw import openclaw_allowed


class OpenClawPolicyTests(unittest.TestCase):
    def test_disabled_when_unconfigured_or_malformed(self):
        for value in ('', ' ', '123,', '123,invalid', '0', '-123'):
            with self.subTest(value=value), patch.dict(os.environ, {'OPENCLAW_ALLOWED_USER_IDS': value}, clear=True):
                self.assertFalse(openclaw_allowed(123, 'origin'))

    def test_only_exact_operator_and_configured_remote(self):
        with patch.dict(os.environ, {'OPENCLAW_ALLOWED_USER_IDS': '123, 456', 'OPENCLAW_REMOTE': 'upstream'}, clear=True):
            self.assertTrue(openclaw_allowed(123, 'upstream'))
            self.assertTrue(openclaw_allowed(456, 'upstream'))
            self.assertFalse(openclaw_allowed(12, 'upstream'))
            self.assertFalse(openclaw_allowed(123, 'origin'))
            self.assertFalse(openclaw_allowed(123, 'https://example.com/repo'))

    def test_malformed_configured_remote_fails_closed(self):
        for value in ('--all', 'https://example.com/repo', '', 'origin\n'):
            with self.subTest(value=value), patch.dict(os.environ, {'OPENCLAW_ALLOWED_USER_IDS': '123', 'OPENCLAW_REMOTE': value}, clear=True):
                self.assertFalse(openclaw_allowed(123, value))

    def test_default_named_remote(self):
        with patch.dict(os.environ, {'OPENCLAW_ALLOWED_USER_IDS': '123'}, clear=True):
            self.assertTrue(openclaw_allowed(123, 'origin'))
