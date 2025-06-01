from __future__ import annotations

import io
from unittest.mock import patch

from chia.cmds.passphrase_funcs import display_passphrase_hint


class TestPassphraseFuncs:
    def test_display_passphrase_hint_with_hint(self):
        """Test that passphrase hint is displayed without using print() for sensitive data."""
        test_hint = "test hint"

        # Mock the Keychain method to return a test hint
        with patch("chia.cmds.passphrase_funcs.Keychain.get_master_passphrase_hint", return_value=test_hint):
            # Capture stdout to verify the output
            captured_output = io.StringIO()
            with patch("sys.stdout", captured_output):
                display_passphrase_hint()

            output = captured_output.getvalue()
            assert f"Passphrase hint: {test_hint}" in output
            assert output.endswith("\n")

    def test_display_passphrase_hint_no_hint(self):
        """Test that appropriate message is shown when no hint is set."""
        # Mock the Keychain method to return None (no hint)
        with patch("chia.cmds.passphrase_funcs.Keychain.get_master_passphrase_hint", return_value=None):
            # Capture stdout to verify the output
            captured_output = io.StringIO()
            with patch("sys.stdout", captured_output):
                display_passphrase_hint()

            output = captured_output.getvalue()
            assert "Passphrase hint is not set" in output

    def test_display_passphrase_hint_uses_stdout_write(self):
        """Test that sensitive hint data is written to stdout directly, not through print()."""
        test_hint = "sensitive test hint"

        with patch("chia.cmds.passphrase_funcs.Keychain.get_master_passphrase_hint", return_value=test_hint):
            # Mock sys.stdout.write to verify it's called directly
            with patch("sys.stdout.write") as mock_write, patch("sys.stdout.flush") as mock_flush:
                display_passphrase_hint()

                # Verify that stdout.write was called with the hint
                mock_write.assert_called_once_with(f"Passphrase hint: {test_hint}\n")
                mock_flush.assert_called_once()
