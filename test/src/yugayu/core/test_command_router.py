from unittest.mock import patch
from yugayu.core.command_router import yugayu_router

# Dummy function to simulate a protected CLI command
@yugayu_router
def dummy_command(ayu_name: str, payload: str):
    return "command_executed"

# Update the patch to target the class method
@patch("yugayu.core.security.identity_verifier.Ed25519Bouncer.verify_identity")
def test_gateway_blocks_invalid_identity(mock_verify, mock_lab):
    # Simulate the IAM check failing by returning False
    mock_verify.return_value = False
    
    # The gateway should intercept this and return None, blocking execution
    result = dummy_command(ayu_name="rogue-agent", payload="malicious-data")
    assert result is None

# Update the patch to target the class method
@patch("yugayu.core.security.identity_verifier.Ed25519Bouncer.verify_identity")
def test_gateway_allows_valid_identity(mock_verify, mock_lab):
    # Simulate a valid cryptographic signature
    mock_verify.return_value = True
    
    # The gateway should allow the command to execute
    result = dummy_command(ayu_name="trusted-agent", payload="safe-data")
    assert result == "command_executed"