import pytest
import yaml
import time
from pathlib import Path
from typer.testing import CliRunner

@pytest.fixture
def mock_lab(tmp_path, monkeypatch):
    """Creates a temporary, sandboxed environment for testing."""
    fake_home = tmp_path / "home"
    fake_lab_root = fake_home / "yugayu-lab"
    fake_home.mkdir(parents=True)
    
    # Force the OS to think /tmp/ is the user's home directory
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    # Mock the environment variable for .expanduser()
    monkeypatch.setenv("HOME", str(fake_home))
    
    # Initialize a base config
    config_dir = fake_home / ".yugayu"
    config_dir.mkdir()
    config_path = config_dir / "config.yaml"
    
    initial_config = {"lab_root": str(fake_lab_root), "ayus": [], "models": []}
    with open(config_path, "w") as f:
        yaml.dump(initial_config, f)
        
    return fake_lab_root

@pytest.fixture
def runner():
    return CliRunner()

def pytest_configure(config):
    """
    Automatically generate a timestamped JUnit XML log for EVERY test run,
    unless the user explicitly provides a different --junitxml path.
    """
    if not config.option.xmlpath:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        log_dir = Path("test/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        config.option.xmlpath = str(log_dir / f"run_{timestamp}.xml")