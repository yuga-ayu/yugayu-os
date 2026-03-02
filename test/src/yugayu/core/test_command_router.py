import json
from pathlib import Path
from unittest.mock import patch
from yugayu.core.command_router import yugayu_router

# Dummy function to simulate a protected CLI command
@yugayu_router
def dummy_command(ayu_name: str, payload: str):
    return "command_executed"

# We must patch the specific Path.exists check used in the router
@patch("yugayu.core.command_router.Path.exists")
def test_gateway_blocks_guest_default(mock_exists, mock_lab):
    # Simulate the admin-identity.json wallet NOT existing
    mock_exists.return_value = False
    
    result = dummy_command(ayu_name="test", payload="test")
    assert result is None  # Blocked by Guest Default

@patch("yugayu.core.command_router.Ed25519Bouncer.verify_identity")
def test_gateway_allows_valid_maintainer(mock_verify, mock_lab):
    # Simulate valid cryptographic payload
    mock_verify.return_value = True
    
    # mock_lab provides a valid 'maintainer' JSON, so router should pass
    result = dummy_command(ayu_name="trusted-agent", payload="safe-data")
    assert result == "command_executed"