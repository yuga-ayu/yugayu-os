import os
import pytest
import yaml
import time
import json
import base64
from pathlib import Path
from typer.testing import CliRunner

# [SECURITY] Force Maintainer Privilege for the CI/CD test runner 
# before yugayu.main is imported by the tests.
os.environ["YUGAYU_DEV"] = "1"

@pytest.fixture
def mock_lab(tmp_path, monkeypatch):
    """Creates a temporary, sandboxed environment for testing."""
    fake_home = tmp_path / "home"
    fake_lab_root = fake_home / "yugayu-lab"
    fake_home.mkdir(parents=True)
    
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    monkeypatch.setenv("HOME", str(fake_home))
    
    config_dir = fake_home / ".yugayu"
    config_dir.mkdir()
    config_path = config_dir / "config.yaml"
    
    initial_config = {"lab_root": str(fake_lab_root), "ayus": [], "models": []}
    with open(config_path, "w") as f:
        yaml.dump(initial_config, f)
        
    # Provision a VALID dummy admin identity to authorize the test suite
    admin_wallet = config_dir / "admin-identity.json"
    valid_json = {
        "entity_id": "admin-cli",
        "role": "maintainer",
        "public_key": base64.b64encode(b"dummy_pub").decode('utf-8'),
        "private_key": base64.b64encode(b"dummy_priv").decode('utf-8')
    }
    admin_wallet.write_text(json.dumps(valid_json))
        
    return fake_lab_root

@pytest.fixture
def runner():
    return CliRunner()

def pytest_configure(config):
    if not config.option.xmlpath:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        log_dir = Path("test/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        config.option.xmlpath = str(log_dir / f"run_{timestamp}.xml")