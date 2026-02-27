from unittest.mock import patch
from typer.testing import CliRunner
from yugayu.main import app

runner = CliRunner()

# Update the patch to target the class method
@patch("yugayu.core.iam_bouncer.Ed25519Bouncer.verify_identity")
@patch("yugayu.commands.create_ayu.load_config") 
@patch("subprocess.run")
def test_create_ayu(mock_subprocess, mock_load_config, mock_verify, tmp_path):
    # 1. Create a fake config object that points to a temporary Pytest directory
    mock_config = mock_load_config.return_value
    mock_config.lab_root = str(tmp_path / "fake-lab")
    mock_config.ayus = []

    # 2. Mock the subprocess and force the IAM gateway to approve
    mock_subprocess.return_value.returncode = 0
    mock_verify.return_value = True
    
    result = runner.invoke(app, ["create-ayu", "test-vision-app"])
    
    assert result.exit_code == 0
    assert "Building ayu test-vision-app" in result.stdout