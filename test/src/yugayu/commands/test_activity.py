from yugayu.main import app
from yugayu.core.logger import get_daily_log_file

def test_activity_reads_logs(runner, mock_lab):
    # 1. Manually write a fake log entry for today
    log_file = get_daily_log_file()
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text("[STATUS: SUCCESS] [CMD: yugayu fake_command]\n")
    
    # 2. Run the activity command to read it
    result = runner.invoke(app, ["activity"])
    
    assert result.exit_code == 0
    assert "fake_command" in result.stdout
