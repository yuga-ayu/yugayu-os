import pytest
from unittest.mock import patch, MagicMock
from yugayu.core.execution.run_engine import generate_image
from yugayu.core.state.ledger_manager import LabConfig, ayuEntry

@patch("yugayu.core.execution.run_engine.subprocess.run")
@patch("yugayu.core.execution.run_engine.load_config")
def test_agnostic_run_engine(mock_load_config, mock_subprocess):
    # Setup mock ledger with an execution command
    mock_config = LabConfig(lab_root="/tmp/lab", ayus=[
        ayuEntry(
            name="test-ayu", 
            path="/tmp/lab/ayus/test-ayu", 
            inference_command="echo '{prompt}' > {output}"
        )
    ])
    mock_load_config.return_value = mock_config
    
    # Setup successful subprocess return
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_subprocess.return_value = mock_process
    
    success = generate_image("test-ayu", "test prompt", "result.txt")
    
    assert success is True
    # Verify the OS executed the exact command string from the ledger
    mock_subprocess.assert_called_once()
    called_args = mock_subprocess.call_args[0][0]
    assert "test prompt" in called_args