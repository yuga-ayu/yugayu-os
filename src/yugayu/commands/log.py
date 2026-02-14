import typer
from rich.console import Console
from yugayu.core.logger import get_daily_log_file

console = Console()

def cli_log(lines: int = typer.Option(20, help="Number of recent log lines to show")):
    """View the most recent activity logs for today."""
    log_file = get_daily_log_file()
    
    if not log_file.exists():
        console.print(f"[yellow]No logs found for today yet at {log_file}.[/yellow]")
        return
        
    try:
        with open(log_file, "r") as f:
            all_lines = f.readlines()
            recent_lines = all_lines[-lines:]
            
        console.print(f"[bold cyan]Showing last {len(recent_lines)} lines from today's log:[/bold cyan]")
        for line in recent_lines:
            console.print(line.strip())
            
    except Exception as e:
        console.print(f"[bold red]Failed to read logs: {e}[/bold red]")