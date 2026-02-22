from unittest.mock import patch
from yugayu.main import app

# We use @patch to prevent the test from actually running 'git init' and 'uv init'
# This keeps the test fast and prevents it from requiring host OS dependencies.
@patch("subprocess.run") 
def test_create_ayu(mock_subprocess, runner, mock_lab):
    mock_subprocess.return_value.returncode = 0
    
    result = runner.invoke(app, ["create-ayu", "test-vision-app"])
    
    assert result.exit_code == 0
    assert "Building ayu test-vision-app" in result.stdout
    
    # Verify the directory scaffolding
    project_path = mock_lab / "ayus" / "test-vision-app"
    assert project_path.exists()
    assert (project_path / "models").exists()
    
    # Verify IAM Identity token was generated
    assert (project_path / ".yugayu-identity").exists()
