import subprocess
from pathlib import Path
from rich.console import Console
from yugayu.core.state_management import load_config

console = Console()

def cli_tree(target: str):
    """Print the directory tree of the current 'repo' or the configured 'lab'."""
    if target == "repo":
        target_path = Path.cwd()
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
        subprocess.run(["tree", "-I", ignore_str], cwd=target_path, check=True)
    except FileNotFoundError:
        console.print("[red]❌ 'tree' command not found. Install via 'sudo apt install tree'.[/red]")
    except Exception as e:
        console.print(f"[red]❌ Error running tree: {e}[/red]")