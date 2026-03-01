import pytest
from typer.testing import CliRunner
from yugayu.main import app
from unittest.mock import patch

runner = CliRunner()

@patch("yugayu.commands.dev_run_test.subprocess.run")
def test_cli_dev_test_success(mock_subprocess, mock_lab):
    # Mock successful test run
    mock_subprocess.return_value.returncode = 0
    
    result = runner.invoke(app, ["run-test"])
    
    assert result.exit_code == 0
    assert "Initiating Lab Diagnostics" in result.stdout
    mock_subprocess.assert_called_once_with(["uv", "run", "pytest", "-v", "-l"], check=True)