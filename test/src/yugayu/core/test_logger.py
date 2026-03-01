import os
import pytest
from pathlib import Path
from unittest.mock import patch
from yugayu.core.logger import setup_logger, log_command, check_log_size_warning
from yugayu.core.state.ledger_manager import load_config

def test_logger_initialization(mock_lab):
    logger = setup_logger()
    assert logger is not None
    assert logger.name == "yugayu_history"

def test_log_command_writes(mock_lab):
    log_command("test_cli_command", status="SUCCESS", origin="test_user")
    logger = setup_logger()
    log_file = logger.handlers[0].baseFilename
    
    with open(log_file, "r") as f:
        content = f.read()
        assert "[CMD: test_cli_command]" in content
        assert "[STATUS: SUCCESS]" in content

@patch("yugayu.core.logger.load_config")
def test_check_log_size_warning(mock_load_config, mock_lab):
    mock_load_config.return_value.max_log_size_mb = 0
    log_command("bloat_command")
    assert check_log_size_warning() is True