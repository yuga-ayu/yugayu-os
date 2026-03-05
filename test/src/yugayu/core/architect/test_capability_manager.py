import pytest
from unittest.mock import patch, MagicMock
from yugayu.core.architect.capability_manager import provision_ayu_from_manifest
from yugayu.core.state.ledger_manager import LabConfig

@patch("yugayu.core.architect.capability_manager.save_config")
@patch("yugayu.core.architect.capability_manager.load_config")
@patch("yugayu.core.architect.capability_manager.issue_identity")
@patch("yugayu.core.architect.capability_manager.subprocess.run")
def test_provision_ayu_success(mock_run, mock_issue, mock_load, mock_save, tmp_path):
    # Use a real LabConfig instance instead of a MagicMock so asdict() works
    mock_config = LabConfig(
        lab_root=str(tmp_path),
        os_source_path=str(tmp_path / "repo"),
        ayus=[]
    )
    mock_load.return_value = mock_config

    manifest = {
        "entity": {"name": "test_ayu"},
        "setup": ["echo 'testing'"],
        "resources": [],
        "execution": {"inference_command": "python run.py"}
    }

    result = provision_ayu_from_manifest("test_ayu", manifest)

    assert result is True
    mock_issue.assert_called_once()
    mock_run.assert_called_once()
    mock_save.assert_called_once() # Verify it attempted to save the ledger
    assert len(mock_config.ayus) == 1
    assert mock_config.ayus[0].name == "test_ayu"