import pytest
from pathlib import Path
from typer.testing import CliRunner
from yugayu.main import app

runner = CliRunner()

# Added mock_lab fixture so the command passes Bouncer authorization
def test_export_state_isolated(tmp_path, monkeypatch, mock_lab):
    # 1. Mock the Current Working Directory to a temporary pytest folder
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)
    
    # 2. Create dummy files in the isolated temp directory
    dummy_py = tmp_path / "dummy.py"
    dummy_py.write_text("print('hello world')")
    
    dummy_md = tmp_path / "README.md"
    dummy_md.write_text("# Test Repo")
    
    # 3. Create an ignored directory to ensure the filter works
    venv_dir = tmp_path / ".venv"
    venv_dir.mkdir()
    ignored_file = venv_dir / "ignored.py"
    ignored_file.write_text("should not be exported")
    
    # 4. Run the command
    result = runner.invoke(app, ["export-state", "--output-file", "test_export.txt"])
    
    # 5. Assertions
    assert result.exit_code == 0
    assert "State exported successfully" in result.stdout
    
    # Updated path logic to look inside the docs/ directory
    export_file = tmp_path / "docs" / "test_export.txt"
    assert export_file.exists()
    
    content = export_file.read_text()
    assert "print('hello world')" in content
    assert "# Test Repo" in content
    assert "should not be exported" not in content