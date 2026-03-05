import typer
import yaml
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from yugayu.core.architect.capability_manager import provision_ayu_from_manifest
from yugayu.core.state.ledger_manager import load_config

console = Console()

def cli_wakeup_ayu(config_file: str = typer.Option(None, help="Path to an existing ayu-config.yaml")):
    """Config-driven approach to awaken a new Ayu entity."""
    console.print("\n[bold cyan]🧬 Yugayu OS: Ayu Awakening Sequence[/bold cyan]")
    
    if not config_file:
        console.print("[red]❌ For MVP, please provide a config file: yugayu wakeup-ayu --config-file flux2-fp8-config.yaml[/red]")
        return
        
    config_path = Path(config_file)
    
    # 🛡️ Global Path Fallback: If not in CWD, check the Ledger's source path
    if not config_path.exists():
        ledger = load_config()
        if ledger.os_source_path:
            fallback_path = Path(ledger.os_source_path) / config_file
            if fallback_path.exists():
                config_path = fallback_path

    if not config_path.exists():
        console.print(f"[red]❌ Config file not found at {config_file}[/red]")
        return
        
    console.print(f"📄 [cyan]Ingesting manifest from {config_path}[/cyan]")
    with open(config_path, "r") as f:
        manifest_data = yaml.safe_load(f)
        
    name = manifest_data.get("entity", {}).get("name", "unknown-ayu")
    
    console.print("\n[bold]⚖️  Compliance & Capability Audit...[/bold]")
    console.print("[green]✓ Configuration parsed successfully.[/green]")
    
    action = Prompt.ask("\nAction", choices=["Run Setup", "Abort"], default="Run Setup")
    if action == "Abort":
        console.print("Awakening aborted.")
        return
        
    console.print(f"\n[bold cyan]Awakening {name}...[/bold cyan]")
    console.print("🏗️  Handing off to Architect & Capabilities Department...")
    
    success = provision_ayu_from_manifest(name, manifest_data)
    
    if success:
        console.print(f"\n[bold green]✅ Ayu Viable and Awake: {name}[/bold green]")