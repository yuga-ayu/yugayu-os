# TODO: [COMPLIANCE] Cryptographic License Ledger: When downloading a base model (e.g., FLUX), require and log its specific license tag (Apache 2.0, MIT, Proprietary).
# TODO: [COMPLIANCE] Block project execution if a commercial Ayu attempts to load a Non-Commercial/Proprietary base model.
import typer
import sys
from rich.console import Console
from rich.panel import Panel
from pathlib import Path
from yugayu.core.state.ledger_manager import load_config, save_config
from yugayu.core.logger import log_command, log_error
from yugayu.core.economy.treasury_wallet import generate_wallet

console = Console()

def cli_setup_lab(
    lab_root: str = typer.Option("~/yugayu-lab", help="Where to build the lab"),
    nas_path: str = typer.Option(None, help="Path to your NAS backup folder"),
    reset: bool = typer.Option(False, help="Overwrite existing config")
):
    """Initialize the Yugayu AI Lab environment and provision admin identity."""
    full_cmd = " ".join(sys.argv)
    
    # Establish the Control Plane directory first
    config_dir = Path.home() / ".yugayu"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    config_path = config_dir / "config.yaml"
    admin_wallet_path = config_dir / "admin-identity.json"
    
    # --- 1. Provision Admin Identity in the Control Plane ---
    if not admin_wallet_path.exists() or reset:
        console.print(f"🔑 [yellow]Provisioning Local Admin Identity in {config_dir}...[/yellow]")
        try:
            # We pass lab_root for standard ayu generation, but custom_path overrides it for the admin
            generate_wallet("admin-cli", Path.home() / "yugayu-lab", custom_path=admin_wallet_path)
            console.print("✅ [green]Cryptographic Master Key issued.[/green]")
        except Exception as e:
            console.print(f"[red]❌ Failed to provision admin identity: {e}[/red]")
            return
    else:
        console.print("✅ [green]Local Admin Master Key already verified.[/green]")

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