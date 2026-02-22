from yugayu.main import app

def test_status_empty_lab(runner, mock_lab):
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "Lab Root:" in result.stdout
    assert "ayus: 0" in result.stdout
