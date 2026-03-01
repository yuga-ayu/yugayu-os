import typer
import subprocess
from rich.console import Console

console = Console()

def cli_dev_run_test():
    """[DEV] Run the Yugayu Pytest test suite."""
    console.print("🧪 [bold cyan]Initiating Lab Diagnostics (Pytest)...[/bold cyan]")
    
    try:
        # Executes the exact command you run manually
        subprocess.run(["uv", "run", "pytest", "-v", "-l"], check=True)
    except subprocess.CalledProcessError as e:
        console.print(f"\n❌ [bold red]Diagnostics failed with exit code {e.returncode}.[/bold red]")
    except Exception as e:
        console.print(f"\n❌ [bold red]System Error: {e}[/bold red]")