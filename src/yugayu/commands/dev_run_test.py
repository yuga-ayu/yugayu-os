import typer
import subprocess
from pathlib import Path
from rich.console import Console
from yugayu.core.state.ledger_manager import load_config

console = Console()

def cli_dev_run_test():
    """[DEV] Run the Yugayu Pytest test suite based on the Ledger path."""
    console.print("🧪 [bold cyan]Initiating Lab Diagnostics (Pytest)...[/bold cyan]")
    
    config = load_config()
    repo_root = config.os_source_path
    
    if not repo_root or not Path(repo_root).exists():
        console.print("❌ [bold red]OS source path not found in Ledger.[/bold red]")
        console.print("💡 [dim]Run `yugayu setup-lab --reset` inside the repo to register it.[/dim]")
        return
            
    try:
        subprocess.run(
            ["uv", "run", "pytest", "-v", "-l"], 
            check=True, 
            cwd=repo_root # Force execution at the registered repo root
        )
    except subprocess.CalledProcessError as e:
        console.print(f"\n❌ [bold red]Diagnostics failed with exit code {e.returncode}.[/bold red]")
    except Exception as e:
        console.print(f"\n❌ [bold red]System Error: {e}[/bold red]")