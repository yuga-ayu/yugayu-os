import typer
import subprocess
from pathlib import Path
from rich.console import Console
from yugayu.core.state.ledger_manager import load_config

console = Console()

def cli_dev_tree(
    target: str = typer.Argument(None, help="Target: 'repo' or 'lab'"),
    repo: bool = typer.Option(False, "--repo", help="Show repository tree"),
    lab: bool = typer.Option(False, "--lab", help="Show physical lab tree")
):
    """[DEV] Visualize the directory structure of the repository or the physical lab."""
    config = load_config()
    
    # Support both the positional argument and the intuitive flag
    if target == "repo" or repo:
        if not config.os_source_path or not Path(config.os_source_path).exists():
            console.print("❌ [red]Repository path not registered in Ledger.[/red]")
            console.print("💡 [dim]Run `yugayu setup-lab --reset` inside your cloned repo to link it.[/dim]")
            return
        target_path = Path(config.os_source_path)
        ignore_str = "venv|.venv|__pycache__|logs|.git|.pytest_cache|instructions|private"
        console.print(f"🌳 [bold cyan]Tree for Yugayu Repository ({target_path})[/bold cyan]")
        
    elif target == "lab" or lab:
        target_path = Path(config.lab_root).expanduser()
        ignore_str = "venv|.venv|__pycache__"
        console.print(f"🌳 [bold cyan]Tree for Yugayu Lab ({target_path})[/bold cyan]")
        
    else:
        console.print("[red]❌ Please specify a target: `yugayu tree --repo` or `yugayu tree --lab`.[/red]")
        return

    try:
        subprocess.run(["tree", str(target_path), "-I", ignore_str], check=True)
    except Exception as e:
        console.print(f"[red]❌ Error executing tree command: {e}[/red]")