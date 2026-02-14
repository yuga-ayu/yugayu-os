import typer
import sys
from rich.console import Console
from rich.panel import Panel
from pathlib import Path
from yugayu.core.config import load_config, save_config
from yugayu.core.logger import log_command, log_error

console = Console()

def cli_init(
    lab_root: str = typer.Option("~/yugayu-lab", help="Where to build the lab"),
    nas_path: str = typer.Option(None, help="Path to your NAS backup folder"),
    reset: bool = typer.Option(False, help="Overwrite existing config")
):
    """Initialize the Yugayu AI Lab environment."""
    full_cmd = " ".join(sys.argv)
    config_path = Path.home() / ".yugayu" / "config.yaml"
    
    if config_path.exists() and not reset:
        console.print(f"[yellow]Found existing config at {config_path}[/yellow]")
        log_command(full_cmd, status="SKIPPED")
        return

    root = Path(lab_root).expanduser()
    
    try:
        root.mkdir(parents=True, exist_ok=True)
        (root / "ayus").mkdir(exist_ok=True)
        (root / "shared" / "models" / "base").mkdir(parents=True, exist_ok=True)
        (root / "shared" / "datasets").mkdir(parents=True, exist_ok=True)
        console.print(f"[green]✅ Created lab structure at: {root}[/green]")
    except Exception as e:
        console.print(f"[red]❌ Failed to create directories: {e}[/red]")
        log_error(full_cmd, str(e))
        return

    config = load_config()
    config.lab_root = str(lab_root)
    if nas_path: config.nas_path = nas_path
    save_config(config)
    
    console.print(Panel.fit(f"Lab Root: {config.lab_root}", title="🎉 Yugayu Initialized", border_style="green"))
    log_command(full_cmd, status="SUCCESS")