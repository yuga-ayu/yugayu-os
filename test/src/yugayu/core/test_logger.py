import logging
from unittest.mock import patch
from yugayu.core.logger import setup_logger, log_command, check_log_size_warning

def test_logger_creation(mock_lab):
    # Test that the logger initializes correctly
    logger = setup_logger()
    assert logger.name == "yugayu_history"
    assert logger.level == logging.INFO
    assert len(logger.handlers) > 0

def test_log_command_writes_to_file(mock_lab):
    # Test that logging actually writes to the chunked file
    log_command("test_cli_command", status="SUCCESS", origin="test_user")
    
    # Setup logger again to get the current file handler path
    logger = setup_logger()
    log_file = logger.handlers[0].baseFilename
    
    with open(log_file, "r") as f:
        content = f.read()
        assert "[CMD: test_cli_command]" in content
        assert "[STATUS: SUCCESS]" in content

@patch("yugayu.core.logger.load_config")
def test_check_log_size_warning(mock_load_config, mock_lab):
    # Mock the config to have a tiny 0MB limit
    mock_load_config.return_value.max_log_size_mb = 0
    
    # Write a log to ensure the file exists and has size
    log_command("bloat_command")
    
    # Because limit is 0, this should immediately return True (warning triggered)
    assert check_log_size_warning() is True
