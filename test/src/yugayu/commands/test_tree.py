from unittest.mock import patch
from typer.testing import CliRunner
from yugayu.main import app

runner = CliRunner()

@patch("yugayu.commands.tree.subprocess.run")
def test_cli_tree_repo(mock_subprocess):
    # Mock a successful subprocess execution
    mock_subprocess.return_value.returncode = 0
    
    result = runner.invoke(app, ["tree", "repo"])
    
    assert result.exit_code == 0
    mock_subprocess.assert_called_once()
    assert "Tree for Yugayu Repository" in result.stdout

@patch("yugayu.commands.tree.load_config")
@patch("yugayu.commands.tree.subprocess.run")
def test_cli_tree_lab(mock_subprocess, mock_load_config, tmp_path):
    # Mock the config to point to a temporary Pytest directory
    mock_config = mock_load_config.return_value
    mock_config.lab_root = str(tmp_path / "fake-lab")
    mock_subprocess.return_value.returncode = 0
    
    result = runner.invoke(app, ["tree", "lab"])
    
    assert result.exit_code == 0
    mock_subprocess.assert_called_once()
    assert "Tree for Yugayu Lab" in result.stdout
    assert "fake-lab" in result.stdout

def test_cli_tree_invalid_target():
    result = runner.invoke(app, ["tree", "invalid-target"])
    
    # It should not fail with an exception, but it should print an error message
    assert result.exit_code == 0
    assert "Target must be 'repo' or 'lab'" in result.stdout