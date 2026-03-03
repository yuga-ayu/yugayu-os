import pytest
from typer.testing import CliRunner
from yugayu.main import app
from unittest.mock import patch

runner = CliRunner()

@patch("yugayu.commands.dev_run_test.subprocess.run")
@patch("yugayu.commands.dev_run_test.load_config")
def test_cli_dev_test_success(mock_load_config, mock_subprocess, mock_lab, tmp_path):
    # Mock the ledger config to return a valid os_source_path for the test
    mock_config = mock_load_config.return_value
    mock_config.os_source_path = str(tmp_path)
    
    mock_subprocess.return_value.returncode = 0
    
    result = runner.invoke(app, ["run-test"])
    
    assert result.exit_code == 0
    assert "Initiating Lab Diagnostics" in result.stdout
    # FIX: Ensure it checks that the subprocess was called with the correct cwd
    mock_subprocess.assert_called_once_with(["uv", "run", "pytest", "-v", "-l"], check=True, cwd=str(tmp_path))