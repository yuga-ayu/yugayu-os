import pytest
from pathlib import Path
from typer.testing import CliRunner
from yugayu.main import app
from yugayu.core.state.ledger_manager import load_config, save_config

runner = CliRunner()

def test_export_state_isolated(tmp_path, monkeypatch, mock_lab):
    # 1. Update the mock ledger to register our sandboxed tmp directory
    config = load_config()
    config.os_source_path = str(tmp_path)
    save_config(config)

    # 2. Create dummy files in the isolated temp directory
    dummy_py = tmp_path / "dummy.py"
    dummy_py.write_text("print('hello world')")
    
    # 3. Create an ignored directory to ensure the filter works
    venv_dir = tmp_path / ".venv"
    venv_dir.mkdir()
    ignored_file = venv_dir / "ignored.py"
    ignored_file.write_text("should not be exported")
    
    # 4. Run the command
    result = runner.invoke(app, ["export-state", "--output", "test_export.txt"])
    
    # 5. Assertions
    assert result.exit_code == 0
    assert "State exported successfully" in result.stdout
    
    export_file = tmp_path / "docs" / "private" / "test_export.txt"
    assert export_file.exists()
    
    content = export_file.read_text()
    assert "print('hello world')" in content
    assert "should not be exported" not in content