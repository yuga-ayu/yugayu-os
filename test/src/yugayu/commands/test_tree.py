from unittest.mock import patch
from typer.testing import CliRunner
from yugayu.main import app

runner = CliRunner()

# Updated patches to dev_tree, and added mock_lab for auth
@patch("yugayu.commands.dev_tree.subprocess.run")
def test_cli_tree_repo(mock_subprocess, mock_lab):
    # Mock a successful subprocess execution
    mock_subprocess.return_value.returncode = 0
    
    result = runner.invoke(app, ["tree", "repo"])
    
    assert result.exit_code == 0
    mock_subprocess.assert_called_once()
    assert "Tree for Yugayu Repository" in result.stdout

@patch("yugayu.commands.dev_tree.load_config")
@patch("yugayu.commands.dev_tree.subprocess.run")
def test_cli_tree_lab(mock_subprocess, mock_load_config, tmp_path, mock_lab):
    # Mock the config to point to a temporary Pytest directory
    mock_config = mock_load_config.return_value
    mock_config.lab_root = str(tmp_path / "fake-lab")
    mock_subprocess.return_value.returncode = 0
    
    result = runner.invoke(app, ["tree", "lab"])
    
    assert result.exit_code == 0
    mock_subprocess.assert_called_once()
    assert "Tree for Yugayu Lab" in result.stdout
    assert "fake-lab" in result.stdout

def test_cli_tree_invalid_target(mock_lab):
    result = runner.invoke(app, ["tree", "invalid-target"])
    
    # It should not fail with an exception, but it should print an error message
    assert result.exit_code == 0
    assert "Target must be 'repo' or 'lab'" in result.stdout