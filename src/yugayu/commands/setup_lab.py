import typer
import sys
from rich.console import Console
from rich.panel import Panel
from pathlib import Path
from yugayu.core.state.ledger_manager import load_config, save_config
from yugayu.core.logger import log_command, log_error
from yugayu.core.security.identity_issuer import issue_identity

console = Console()

def is_editable_install() -> bool:
    """
    Determines if the OS was installed via `uv tool install -e .`
    by checking if this executed file lives inside a Git repository.
    """
    current_file = Path(__file__).resolve()
    # Path: src/yugayu/commands/setup_lab.py -> 3 parents up is the repo root
    possible_repo_root = current_file.parents[3]
    return (possible_repo_root / ".git").exists()

def cli_setup_lab(
    lab_root: str = typer.Option("~/yugayu-lab", help="Where to build the lab"),
    nas_path: str = typer.Option(None, help="Path to your NAS backup folder"),
    reset: bool = typer.Option(False, help="Overwrite existing config")
):
    """Initialize the Yugayu AI Lab environment and provision admin identity."""
    full_cmd = " ".join(sys.argv)
    
    config_dir = Path.home() / ".yugayu"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    config_path = config_dir / "config.yaml"
    admin_wallet_path = config_dir / "admin-identity.json"
    
    # --- 1. Provision Identity using the Issuer Department ---
    if not admin_wallet_path.exists() or reset:
        console.print(f"🔑 [yellow]Provisioning Local Identity in {config_dir}...[/yellow]")
        try:
            # Dynamically assign role based on install type
            assigned_role = "maintainer" if is_editable_install() else "admin"
            
            if assigned_role == "maintainer":
                console.print("🛠️  [cyan]Editable install detected. Issuing 'maintainer' clearance.[/cyan]")
            else:
                console.print("🏢 [cyan]Standard install detected. Issuing 'admin' clearance.[/cyan]")
                
            issue_identity("admin-cli", assigned_role, custom_path=admin_wallet_path)
            console.print(f"✅ [green]Cryptographic Master Key ({assigned_role}) issued.[/green]")
        except Exception as e:
            console.print(f"[red]❌ Failed to provision identity: {e}[/red]")
            return
    else:
        console.print("✅ [green]Local Identity Master Key already verified.[/green]")

    # --- 2. Initialize Config & Physical Lab Directories ---
    if config_path.exists() and not reset:
        console.print(f"[yellow]Found existing lab config at {config_path}[/yellow]")
        log_command(full_cmd, status="SKIPPED")
        return

    root = Path(lab_root).expanduser()
    
    try:
        root.mkdir(parents=True, exist_ok=True)
        (root / "ayus").mkdir(exist_ok=True)
        (root / "shared" / "models" / "base").mkdir(parents=True, exist_ok=True)
        (root / "shared" / "datasets").mkdir(parents=True, exist_ok=True)
        console.print(f"[green]✅ Created physical lab structure at: {root}[/green]")
    except Exception as e:
        console.print(f"[red]❌ Failed to create directories: {e}[/red]")
        log_error(full_cmd, str(e))
        return

    config = load_config()
    config.lab_root = str(lab_root)
    if nas_path: config.nas_path = nas_path
    save_config(config)
    
    console.print(Panel.fit(f"Control Plane: {config_dir}\nLab Root: {config.lab_root}", title="🎉 Yugayu OS Initialized", border_style="green"))
    log_command(full_cmd, status="SUCCESS")
    