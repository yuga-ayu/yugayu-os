import pytest
import yaml
from pathlib import Path
from typer.testing import CliRunner
from yugayu.main import app
from unittest.mock import patch

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