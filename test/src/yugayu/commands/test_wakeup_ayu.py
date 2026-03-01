import pytest
from typer.testing import CliRunner
from yugayu.main import app
from unittest.mock import patch

runner = CliRunner()

def test_wakeup_ayu_aborted(monkeypatch, mock_lab):
    # Simulate choosing '1' (Genesis), entering details, but aborting at confirmation
    inputs = "1\ntest-vision\nhf.co/model\nN\n"
    result = runner.invoke(app, ["wakeup-ayu"], input=inputs)
    
    assert result.exit_code == 0
    assert "Awakening aborted" in result.stdout

def test_wakeup_ayu_success(monkeypatch, mock_lab):
    # Simulate choosing '1', entering details, and confirming (Y)
    inputs = "1\ntest-vision\nhf.co/model\nY\n"
    result = runner.invoke(app, ["wakeup-ayu"], input=inputs)
    
    assert result.exit_code == 0
    assert "Compliance audit passed" in result.stdout
    assert "Ayu Viable and Awake" in result.stdout
    assert "Name: test-vision" in result.stdout

def test_wakeup_ayu_locked_vector(mock_lab):
    # Simulate trying to use an unavailable vector (2)
    result = runner.invoke(app, ["wakeup-ayu"], input="2\n")
    assert result.exit_code == 0
    assert "Vector currently locked by Core" in result.stdout