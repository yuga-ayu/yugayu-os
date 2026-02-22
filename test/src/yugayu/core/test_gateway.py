import pytest
from unittest.mock import patch
from yugayu.core.gateway import yugayu_gateway

# Create a dummy command to wrap with our gateway
@yugayu_gateway
def dummy_command():
    return "command_executed"

@patch("yugayu.core.gateway.verify_identity")
@patch("yugayu.core.gateway.console.print")
def test_gateway_blocks_invalid_identity(mock_print, mock_verify, mock_lab):
    # 1. Simulate the IAM check failing
    mock_verify.return_value = False
    
    result = dummy_command()
    
    # Assert the command was completely blocked (returned None)
    assert result is None
    
    # Assert the correct AuthError was printed to the terminal
    mock_print.assert_called_once()
    assert "AuthError" in mock_print.call_args[0][0]

@patch("yugayu.core.gateway.verify_identity")
@patch("yugayu.core.gateway.check_log_size_warning")
@patch("yugayu.core.gateway.console.print")
def test_gateway_allows_valid_identity_with_log_warning(mock_print, mock_check_size, mock_verify, mock_lab):
    # 2. Simulate IAM passing, but logs are too big
    mock_verify.return_value = True
    mock_check_size.return_value = True
    
    result = dummy_command()
    
    # Assert the command STILL EXECUTED
    assert result == "command_executed"
    
    # Assert the maintenance warning was printed
    mock_print.assert_called_once()
    assert "WARNING" in mock_print.call_args[0][0]

@patch("yugayu.core.gateway.verify_identity")
@patch("yugayu.core.gateway.check_log_size_warning")
@patch("yugayu.core.gateway.console.print")
def test_gateway_clean_execution(mock_print, mock_check_size, mock_verify, mock_lab):
    # 3. Simulate perfect conditions: IAM passes, logs are small
    mock_verify.return_value = True
    mock_check_size.return_value = False
    
    result = dummy_command()
    
    # Assert the command executed cleanly
    assert result == "command_executed"
    
    # Assert absolutely nothing was printed to the console (silent operation)
    mock_print.assert_not_called()
