import os
import pytest
from pathlib import Path
from yugayu.core.state.ledger_manager import load_config, save_config, LabConfig, ayuEntry

def test_config_lifecycle(mock_lab):
    # 1. Test loading a non-existent config (should create defaults)
    config = load_config()
    assert config.lab_root.endswith("yugayu-lab")
    assert len(config.ayus) == 0
    
    # 2. Test saving and modifying config
    new_ayu = ayuEntry(name="test-vision", path="/fake/path")
    config.ayus.append(new_ayu)
    config.max_log_size_mb = 500
    save_config(config)
    
    # 3. Test reloading the saved config
    reloaded_config = load_config()
    assert len(reloaded_config.ayus) == 1
    assert reloaded_config.ayus[0].name == "test-vision"
    assert reloaded_config.max_log_size_mb == 500