from unittest.mock import patch
from yugayu.core.security.enforcer import quarantine_entity
from yugayu.core.state.ledger_manager import load_config, LabConfig, ayuEntry

@patch("yugayu.core.security.enforcer.save_config")
@patch("yugayu.core.security.enforcer.load_config")
def test_quarantine_existing_entity(mock_load, mock_save):
    # 1. Setup mock config with an active Ayu
    mock_config = LabConfig(lab_root="/tmp/lab", ayus=[ayuEntry(name="rogue-ayu", path="/tmp", status="active")])
    mock_load.return_value = mock_config
    
    # 2. Trigger enforcer
    quarantine_entity("rogue-ayu", "Malicious payload detected")
    
    # 3. Assert status was changed and saved
    assert mock_config.ayus[0].status == "quarantined"
    mock_save.assert_called_once_with(mock_config)

@patch("yugayu.core.security.enforcer.save_config")
@patch("yugayu.core.security.enforcer.load_config")
def test_quarantine_unknown_entity(mock_load, mock_save):
    # 1. Setup mock config with NO matching Ayu
    mock_config = LabConfig(lab_root="/tmp/lab", ayus=[])
    mock_load.return_value = mock_config
    
    # 2. Trigger enforcer on an unknown external actor
    quarantine_entity("unknown-hacker", "Intrusion attempt")
    
    # 3. Assert config wasn't saved (since nothing in ledger was modified)
    mock_save.assert_not_called()