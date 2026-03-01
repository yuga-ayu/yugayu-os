import subprocess
import os
from pathlib import Path
from rich.console import Console
from yugayu.core.state.ledger_manager import load_config

console = Console()

def find_repo_root():
    """Traverse up to find the pyproject.toml which marks the repo root."""
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        if (parent / "pyproject.toml").exists():
            return parent
    return current

def cli_dev_tree(target: str):
    if target == "repo":
        target_path = find_repo_root()
        ignore_str = "venv|__pycache__|logs|.git"
        console.print(f"🌳 [bold cyan]Tree for Yugayu Repository ({target_path})[/bold cyan]")
    elif target == "lab":
        config = load_config()
        target_path = Path(config.lab_root).expanduser()
        ignore_str = "venv|__pycache__"
        console.print(f"🌳 [bold cyan]Tree for Yugayu Lab ({target_path})[/bold cyan]")
    else:
        console.print("[red]❌ Target must be 'repo' or 'lab'.[/red]")
        return

    try:
        subprocess.run(["tree", str(target_path), "-I", ignore_str], check=True)
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")