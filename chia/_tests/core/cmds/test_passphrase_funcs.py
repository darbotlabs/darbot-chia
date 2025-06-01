from __future__ import annotations

import io
from unittest.mock import patch

from chia.cmds.passphrase_funcs import display_passphrase_hint, prompt_for_new_passphrase


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

    def test_prompt_for_new_passphrase_error_uses_stdout_write(self):
        """Test that passphrase validation errors are written to stdout directly, not through print()."""
        # Mock getpass to return mismatched passphrases
        with patch("chia.cmds.passphrase_funcs.getpass") as mock_getpass:
            # Mock supports_os_passphrase_storage to return False to avoid prompting for save
            with patch("chia.cmds.passphrase_funcs.supports_os_passphrase_storage", return_value=False):
                # Set up getpass to return different passphrases first, then matching ones
                mock_getpass.side_effect = ["password1", "password2", "password", "password"]
                
                # Mock sys.stdout.write to verify it's called directly for error messages
                with patch("sys.stdout.write") as mock_write, patch("sys.stdout.flush") as mock_flush:
                    result = prompt_for_new_passphrase()
                    
                    # Verify that stdout.write was called with the error message
                    mock_write.assert_called_with("Passphrases do not match\n")
                    mock_flush.assert_called()
                    
                    # Verify the function eventually returns valid result
                    assert result[0] == "password"
                    assert result[1] is False
