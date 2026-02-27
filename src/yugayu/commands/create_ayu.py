# TODO: [TRACKING] Shared Resource Ledger: Create a symlink map tracking which Ayus depend on which shared /models/base weights.
# TODO: [TRACKING] Dependency Graph: Prevent deletion of a base model if active Ayus are still linked to it.

import sys
import subprocess
import uuid
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from yugayu.core.state_management import load_config, save_config, ayuEntry
from yugayu.core.logger import log_command, log_error

console = Console()

def cli_create_ayu(ayu_name: str):
    """Scaffold a new AI ayu with Git, UV, and an IAM Identity."""
    full_cmd = " ".join(sys.argv)
    
    config = load_config()
    lab_root = Path(config.lab_root).expanduser()
    ayu_path = lab_root / "ayus" / ayu_name
    
    if ayu_path.exists():
        console.print(f"[red]❌ ayu directory '{ayu_name}' already exists![/red]")
        log_error(full_cmd, "Directory exists")
        return
        
    try:
        console.print(f"🏗️  Building ayu [bold cyan]{ayu_name}[/bold cyan]...")
        ayu_path.mkdir(parents=True)
        (ayu_path / "models").mkdir()
        (ayu_path / "dataset").mkdir()
        (ayu_path / "outputs").mkdir()
        (ayu_path / "recipes").mkdir()
        
        subprocess.run(["git", "init"], cwd=ayu_path, check=True, capture_output=True)
        console.print("   [green]✔[/green] Initialized Git repository")
        
        subprocess.run(["uv", "init"], cwd=ayu_path, check=True, capture_output=True)
        console.print("   [green]✔[/green] Initialized UV Python environment")
        
        identity_token = str(uuid.uuid4())
        identity_file = ayu_path / ".yugayu-identity"
        with open(identity_file, "w") as f:
            f.write(f"ayu={ayu_name}\nROLE=standard_ayu\nTOKEN={identity_token}\n")
        
        with open(ayu_path / ".gitignore", "a") as f:
            f.write("\n# Yugayu IAM\n.yugayu-identity\n")
        console.print("   [green]✔[/green] Generated ayu Identity Wallet")
        
        new_ayu = ayuEntry(name=ayu_name, path=str(ayu_path))
        config.ayus.append(new_ayu)
        save_config(config)
        console.print("   [green]✔[/green] Registered in Lab Config")

        console.print(Panel.fit(f"Run: [bold]cd {ayu_path}[/bold]", title="🚀 ayu Created Successfully", border_style="blue"))
        log_command(full_cmd, status="SUCCESS")
        
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ Subprocess failed: {e.stderr.decode()}[/red]")
        log_error(full_cmd, f"Subprocess failed: {e}")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        log_error(full_cmd, str(e))
