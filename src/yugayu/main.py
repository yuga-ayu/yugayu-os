import typer
import sys
from rich.console import Console
from rich.panel import Panel
from pathlib import Path
from yugayu.config import load_config, save_config

# Import our new logging engine
from yugayu.logger import log_command, log_error, check_log_size_warning, get_daily_log_file

app = typer.Typer()
console = Console()

def check_logs():
    """Helper to warn the user if logs are getting too large."""
    if check_log_size_warning():
        console.print("[bold red]⚠️ WARNING:[/bold red] [yellow]Your Yugayu logs have exceeded the maximum size limit. Consider backing them up to your NAS.[/yellow]\n")

@app.command()
def init(
    lab_root: str = typer.Option("~/yugayu-lab", help="Where to build the lab"),
    nas_path: str = typer.Option(None, help="Path to your NAS backup folder"),
    reset: bool = typer.Option(False, help="Overwrite existing config")
):
    """
    Initialize the Yugayu AI Lab environment.
    """
    full_cmd = " ".join(sys.argv)
    check_logs()
    
    config_path = Path.home() / ".yugayu" / "config.yaml"
    
    if config_path.exists() and not reset:
        console.print(f"[yellow]Found existing config at {config_path}[/yellow]")
        log_command(full_cmd, status="SKIPPED (Already exists)")
        return

    root = Path(lab_root).expanduser()
    
    try:
        root.mkdir(parents=True, exist_ok=True)
        (root / "projects").mkdir(exist_ok=True)
        (root / "shared" / "models" / "base").mkdir(parents=True, exist_ok=True)
        (root / "shared" / "datasets").mkdir(parents=True, exist_ok=True)
        console.print(f"[green]✅ Created lab structure at: {root}[/green]")
    except Exception as e:
        console.print(f"[red]❌ Failed to create directories: {e}[/red]")
        log_error(full_cmd, str(e))
        return

    config = load_config()
    config.lab_root = str(lab_root)
    if nas_path:
        config.nas_path = nas_path
        
    save_config(config)
    
    console.print(Panel.fit(
        f"Lab Root: {config.lab_root}\nNAS Path: {config.nas_path or 'Not Set'}",
        title="🎉 Yugayu Initialized",
        border_style="green"
    ))
    
    log_command(full_cmd, status="SUCCESS")

@app.command()
def info():
    """Show current lab status."""
    full_cmd = " ".join(sys.argv)
    check_logs()
    
    try:
        cfg = load_config()
        console.print(f"[bold]Lab Root:[/bold] {cfg.lab_root}")
        console.print(f"[bold]Projects:[/bold] {len(cfg.projects)}")
        log_command(full_cmd)
    except Exception as e:
        log_error(full_cmd, str(e))

@app.command()
def log(lines: int = typer.Option(20, help="Number of recent log lines to show")):
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

if __name__ == "__main__":
    app()
