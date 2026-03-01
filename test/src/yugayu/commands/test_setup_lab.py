from yugayu.main import app

def test_setup_lab(runner, mock_lab):
    # Run the setup command
    result = runner.invoke(app, ["setup-lab", "--reset"])
    
    assert result.exit_code == 0
    # Updated string match to match the new output
    assert "Created physical lab structure at" in result.stdout
    
    # Verify the physical directories were created in the mock lab
    assert (mock_lab / "ayus").exists()
    assert (mock_lab / "shared" / "models" / "base").exists()
    assert (mock_lab / "shared" / "datasets").exists()