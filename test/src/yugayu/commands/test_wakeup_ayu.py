import pytest
import yaml
from pathlib import Path
from typer.testing import CliRunner
from yugayu.main import app
from unittest.mock import patch
import json

runner = CliRunner()

def test_wakeup_ayu_no_config(mock_lab):
    # Ensure it fails safely if no config is provided
    result = runner.invoke(app, ["wakeup-ayu"])
    assert result.exit_code == 0
    assert "please provide a config file" in result.stdout

@patch('yugayu.commands.wakeup_ayu.provision_ayu_from_manifest', return_value=True)
def test_wakeup_ayu_success(mock_provision, mock_lab, tmp_path):
    # 1. Create a mock config file dynamically during the test
    config_file = tmp_path / "mock-config.yaml"
    mock_manifest = {"entity": {"name": "test-vision"}, "resources": []}
    with open(config_file, "w") as f:
        yaml.dump(mock_manifest, f)

    # 2. Run the command, confirming the "Run Setup" prompt
    result = runner.invoke(app, ["wakeup-ayu", "--config-file", str(config_file)], input="Run Setup\n")
    
    assert result.exit_code == 0
    assert "Ingesting manifest" in result.stdout
    assert "Ayu Viable and Awake: test-vision" in result.stdout
    mock_provision.assert_called_once()
    
@patch('yugayu.commands.wakeup_ayu.provision_ayu_from_manifest', return_value=False)
def test_wakeup_ayu_aborted_by_prompt(mock_provision, mock_lab, tmp_path):
    # 1. Create a mock config file
    config_file = tmp_path / "mock-config.yaml"
    mock_manifest = {"entity": {"name": "test-vision"}, "resources": []}
    with open(config_file, "w") as f:
        yaml.dump(mock_manifest, f)

    # 2. Input "Abort" at the execution prompt
    result = runner.invoke(app, ["wakeup-ayu", "--config-file", str(config_file)], input="Abort\n")
    
    assert result.exit_code == 0
    assert "Awakening aborted." in result.stdout
    mock_provision.assert_not_called()

@patch('yugayu.commands.wakeup_ayu.load_config')
@patch('yugayu.commands.wakeup_ayu.Prompt.ask', return_value="Run Setup")
@patch('yugayu.commands.wakeup_ayu.provision_ayu_from_manifest', return_value=True)
@patch('yugayu.core.command_router.Path.home') # <-- Intercepts the router's path
@patch('yugayu.core.command_router.Ed25519Bouncer.verify_identity', return_value=True) # <-- Bypasses crypto validation
def test_wakeup_ayu_ledger_path_fallback(mock_bouncer, mock_home, mock_provision, mock_prompt, mock_load, tmp_path, monkeypatch):
    """Verifies the CLI can find the config via the ledger if run from an external directory."""
    
    # 0. Satisfy the Zero-Trust Middleware Router
    mock_home.return_value = tmp_path
    config_dir = tmp_path / ".yugayu"
    config_dir.mkdir(parents=True, exist_ok=True)
    wallet_path = config_dir / "admin-identity.json"
    wallet_path.write_text('{"role": "admin", "entity_id": "admin-cli"}')

    # 1. Create a fake repo root and config file
    fake_repo = tmp_path / "fake_repo"
    fake_repo.mkdir()
    config_file = fake_repo / "my_config.yaml"
    config_file.write_text("entity:\n  name: test-ayu")

    # 2. Move the terminal's current working directory somewhere completely different
    external_dir = tmp_path / "some_other_folder"
    external_dir.mkdir()
    monkeypatch.chdir(external_dir)

    # 3. Mock the ledger to point to the fake repo
    mock_config = mock_load.return_value
    mock_config.os_source_path = str(fake_repo)

    # 4. Execute the command using just the relative filename
    # Assuming 'app' and 'runner' are imported/defined in your test file context
    result = runner.invoke(app, ["wakeup-ayu", "--config-file", "my_config.yaml"])

    assert result.exit_code == 0
    assert "Ingesting manifest" in result.stdout