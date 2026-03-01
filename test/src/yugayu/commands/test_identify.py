import pytest
from typer.testing import CliRunner
from yugayu.main import app
from unittest.mock import patch

runner = CliRunner()

@patch('yugayu.core.command_router.Ed25519Bouncer.verify_identity', return_value=True)
def test_identify_command(mock_verify):
    # Simulate querying the ledger for an entity
    result = runner.invoke(app, ["identify", "test-entity"])
    
    assert result.exit_code == 0
    assert "Querying Merkle Ledger for 'test-entity'" in result.stdout
    assert "Cryptographic Identity Card:" in result.stdout
    assert "Entity: test-entity" in result.stdout