import pytest
from typer.testing import CliRunner
from yugayu.main import app
from unittest.mock import patch

runner = CliRunner()

@patch('yugayu.core.command_router.Ed25519Bouncer.verify_identity', return_value=True)
@patch('yugayu.commands.ask.generate_image', return_value=True)
def test_ask_command_success(mock_generate, mock_verify, mock_lab):
    result = runner.invoke(app, ["ask", "test-ayu", "test prompt"])
    
    assert result.exit_code == 0
    assert "Routing payload to test-ayu" in result.stdout
    assert "Task complete" in result.stdout
    mock_generate.assert_called_once_with("test-ayu", "test prompt", "./result.png", None)

@patch('yugayu.core.command_router.Ed25519Bouncer.verify_identity', return_value=True)
@patch('yugayu.commands.ask.generate_image', return_value=False)
def test_ask_command_failure(mock_generate, mock_verify, mock_lab):
    result = runner.invoke(app, ["ask", "test-ayu", "test prompt"])
    
    assert result.exit_code == 0
    assert "Execution failed" in result.stdout