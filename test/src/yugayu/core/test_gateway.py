from unittest.mock import patch, MagicMock
from yugayu.core.gateway import yugayu_gateway

# Dummy function to simulate a protected CLI command
@yugayu_gateway
def dummy_command(ayu_name: str, payload: str):
    return "command_executed"

@patch("yugayu.core.gateway.verify_identity")
def test_gateway_blocks_invalid_identity(mock_verify):
    # Simulate the IAM check failing by returning False
    mock_verify.return_value = False
    
    # The gateway should intercept this and return None, blocking execution
    result = dummy_command(ayu_name="rogue-agent", payload="malicious-data")
    assert result is None

@patch("yugayu.core.gateway.verify_identity")
def test_gateway_allows_valid_identity(mock_verify):
    # Simulate a valid cryptographic signature
    mock_verify.return_value = True
    
    # The gateway should allow the command to execute
    result = dummy_command(ayu_name="trusted-agent", payload="safe-data")
    assert result == "command_executed"