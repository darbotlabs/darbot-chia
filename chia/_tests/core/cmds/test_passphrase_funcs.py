from __future__ import annotations

import io
from unittest.mock import patch, call

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

    def test_prompt_for_new_passphrase_uses_stdout_write_for_length_requirement(self):
        """Test that minimum passphrase length requirement is written to stdout directly, not through print()."""
        min_length = 12
        
        # Mock dependencies
        with patch("chia.cmds.passphrase_funcs.Keychain.minimum_passphrase_length", return_value=min_length), \
             patch("chia.cmds.passphrase_funcs.getpass") as mock_getpass, \
             patch("chia.cmds.passphrase_funcs.verify_passphrase_meets_requirements", return_value=(True, None)), \
             patch("chia.cmds.passphrase_funcs.supports_os_passphrase_storage", return_value=False), \
             patch("sys.stdout.write") as mock_write, \
             patch("sys.stdout.flush") as mock_flush:
            
            # Set up getpass to return valid passphrases
            mock_getpass.side_effect = ["test_passphrase", "test_passphrase"]
            
            # Call the function
            result = prompt_for_new_passphrase()
            
            # Verify that stdout.write was called with the length requirement
            mock_write.assert_called_once_with(f"\nPassphrases must be {min_length} or more characters in length\n")
            mock_flush.assert_called_once()
            
            # Verify function returns expected result
            assert result == ("test_passphrase", False)

    def test_prompt_for_new_passphrase_no_length_requirement(self):
        """Test that no output is written when minimum passphrase length is 0."""
        min_length = 0
        
        # Mock dependencies
        with patch("chia.cmds.passphrase_funcs.Keychain.minimum_passphrase_length", return_value=min_length), \
             patch("chia.cmds.passphrase_funcs.getpass") as mock_getpass, \
             patch("chia.cmds.passphrase_funcs.verify_passphrase_meets_requirements", return_value=(True, None)), \
             patch("chia.cmds.passphrase_funcs.supports_os_passphrase_storage", return_value=False), \
             patch("sys.stdout.write") as mock_write, \
             patch("sys.stdout.flush") as mock_flush:
            
            # Set up getpass to return valid passphrases
            mock_getpass.side_effect = ["test_passphrase", "test_passphrase"]
            
            # Call the function
            result = prompt_for_new_passphrase()
            
            # Verify that stdout.write was NOT called since min_length is 0
            mock_write.assert_not_called()
            mock_flush.assert_not_called()
            
            # Verify function returns expected result
            assert result == ("test_passphrase", False)

    def test_prompt_for_new_passphrase_error_message_uses_stdout_write(self):
        """Test that error messages containing sensitive info are written to stdout directly."""
        min_length = 12
        error_message = f"Minimum passphrase length is {min_length}"
        
        # Mock dependencies to simulate a passphrase validation error
        with patch("chia.cmds.passphrase_funcs.Keychain.minimum_passphrase_length", return_value=min_length), \
             patch("chia.cmds.passphrase_funcs.getpass") as mock_getpass, \
             patch("chia.cmds.passphrase_funcs.verify_passphrase_meets_requirements") as mock_verify, \
             patch("sys.stdout.write") as mock_write, \
             patch("sys.stdout.flush") as mock_flush:
            
            # Set up getpass to return passphrases (one invalid, one valid)
            mock_getpass.side_effect = ["short", "short", "valid_passphrase", "valid_passphrase"]
            
            # Set up verification to fail first time, succeed second time
            mock_verify.side_effect = [(False, error_message), (True, None)]
            
            # Call the function
            result = prompt_for_new_passphrase()
            
            # Verify that stdout.write was called for both length requirement and error message
            expected_calls = [
                call(f"\nPassphrases must be {min_length} or more characters in length\n"),
                call(f"{error_message}\n")
            ]
            assert mock_write.call_count == 2
            mock_write.assert_has_calls(expected_calls)
            assert mock_flush.call_count == 2
            
            # Verify function returns expected result
            assert result == ("valid_passphrase", False)
