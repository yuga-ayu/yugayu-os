import pytest
from unittest.mock import patch
from pathlib import Path
from typer.testing import CliRunner
from yugayu.main import app

runner = CliRunner()

@patch("yugayu.core.command_router.Ed25519Bouncer.verify_identity", return_value=True)
def test_verify_lab_success(mock_verify, mock_lab):
    # Physically create the expected lab structure inside the Pytest temporary folder
    (mock_lab / "ayus").mkdir(parents=True, exist_ok=True)
    (mock_lab / "shared" / "models" / "base").mkdir(parents=True, exist_ok=True)
    (mock_lab / "shared" / "datasets").mkdir(parents=True, exist_ok=True)
    
    result = runner.invoke(app, ["verify-lab"])
        
    assert result.exit_code == 0
    assert "Verification Complete: Lab is 100% Viable" in result.stdout
    assert "Merkle Ledger (config.yaml) intact" in result.stdout

@patch("yugayu.core.command_router.Ed25519Bouncer.verify_identity", return_value=True)
def test_verify_lab_missing_config(mock_verify, mock_lab):
    # Physically delete the sandbox ledger that mock_lab created
    config_path = Path.home() / ".yugayu" / "config.yaml"
    if config_path.exists():
        config_path.unlink()
        
    result = runner.invoke(app, ["verify-lab"])
    
    assert result.exit_code == 0
    assert "Merkle Ledger missing" in result.stdout
    # The script safely aborts here, so we do not check for the final anomaly tally.