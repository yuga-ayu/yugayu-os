from unittest.mock import patch
from typer.testing import CliRunner
from yugayu.main import app

runner = CliRunner()

@patch("yugayu.commands.dev_tree.load_config")
@patch("yugayu.commands.dev_tree.subprocess.run")
def test_cli_tree_repo(mock_subprocess, mock_load_config, mock_lab, tmp_path):
    # Fixed: Provide a valid os_source_path to the mocked ledger
    mock_config = mock_load_config.return_value
    mock_config.os_source_path = str(tmp_path)
    mock_subprocess.return_value.returncode = 0
    
    result = runner.invoke(app, ["tree", "repo"])
    
    assert result.exit_code == 0
    mock_subprocess.assert_called_once()
    assert "Tree for Yugayu Repository" in result.stdout

@patch("yugayu.commands.dev_tree.load_config")
@patch("yugayu.commands.dev_tree.subprocess.run")
def test_cli_tree_lab(mock_subprocess, mock_load_config, mock_lab, tmp_path):
    mock_config = mock_load_config.return_value
    mock_config.lab_root = str(tmp_path / "fake-lab")
    mock_subprocess.return_value.returncode = 0
    
    result = runner.invoke(app, ["tree", "lab"])
    
    assert result.exit_code == 0
    mock_subprocess.assert_called_once()
    assert "Tree for Yugayu Lab" in result.stdout

def test_cli_tree_invalid_target(mock_lab):
    result = runner.invoke(app, ["tree", "invalid-target"])
    
    assert result.exit_code == 0
    # Fixed: Match the new error string
    assert "Please specify a target" in result.stdout