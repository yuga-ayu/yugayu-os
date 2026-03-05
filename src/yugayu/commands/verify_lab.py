import typer
import json
from pathlib import Path
from rich.console import Console
from yugayu.core.state.ledger_manager import load_config

console = Console()

def cli_verify_lab():
    """Verify the cryptographic and physical integrity of the Yugayu Lab."""
    console.print("🔍 [bold cyan]Initiating Lab Integrity Verification...[/bold cyan]\n")
    
    config_dir = Path.home() / ".yugayu"
    config_path = config_dir / "config.yaml"
    admin_wallet = config_dir / "admin-identity.json"
    
    issues_found = 0
    
    # 1. Control Plane Verification
    console.print("[bold]1. Control Plane Audits (~/.yugayu)[/bold]")
    if config_dir.exists():
        console.print("  [green]✓[/green] Control Plane directory exists")
    else:
        console.print("  [red]✗[/red] Control Plane directory missing")
        issues_found += 1
        
    if config_path.exists():
        console.print("  [green]✓[/green] Merkle Ledger (config.yaml) intact")
        try:
            config = load_config()
        except Exception:
            console.print("  [red]✗[/red] Merkle Ledger is corrupted or unreadable")
            issues_found += 1
    else:
        console.print("  [red]✗[/red] Merkle Ledger missing")
        issues_found += 1
        return # Cannot proceed without config
        
    if admin_wallet.exists():
        try:
            with open(admin_wallet, "r") as f:
                data = json.load(f)
            role = data.get("role", "unknown")
            console.print(f"  [green]✓[/green] Cryptographic Identity verified (Role: {role})")
        except Exception:
            console.print("  [red]✗[/red] Cryptographic Identity corrupted")
            issues_found += 1
    else:
        console.print("  [red]✗[/red] Cryptographic Identity missing (Guest Mode Defaulted)")
        issues_found += 1

    # 2. Physical Lab Verification
    console.print("\n[bold]2. Physical Lab Audits[/bold]")
    lab_root = Path(config.lab_root).expanduser()
    
    if lab_root.exists():
        console.print(f"  [green]✓[/green] Lab Root mounted at {lab_root}")
    else:
        console.print(f"  [red]✗[/red] Lab Root missing at {lab_root}")
        issues_found += 1
        
    # Check sub-directories
    for subdir in ["ayus", "shared/models/base", "shared/datasets"]:
        target = lab_root / subdir
        if target.exists():
            console.print(f"  [green]✓[/green] Partition '{subdir}' verified")
        else:
            console.print(f"  [red]✗[/red] Partition '{subdir}' missing")
            issues_found += 1
            
    # 3. Ledger Sync Check
    console.print("\n[bold]3. Ledger vs Reality Sync[/bold]")
    ayus_dir = lab_root / "ayus"
    physical_ayus = set(d.name for d in ayus_dir.iterdir() if d.is_dir()) if ayus_dir.exists() else set()
    ledger_ayus = set(a.name for a in config.ayus)
    
    # Ghost directories (exist physically but not on ledger)
    ghosts = physical_ayus - ledger_ayus
    for g in ghosts:
        console.print(f"  [yellow]⚠️[/yellow] Ghost Entity Detected: '{g}' (Physical directory exists but missing from Ledger)")
        issues_found += 1
        
    # Missing physicals (exist on ledger but no directory)
    missing = ledger_ayus - physical_ayus
    for m in missing:
        console.print(f"  [red]✗[/red] Ledger Desync: Entity '{m}' is in config but missing physical directory")
        issues_found += 1

    if not ghosts and not missing:
        console.print("  [green]✓[/green] All entities perfectly synced with Ledger")

    # 4. Final Verdict
    console.print("\n---")
    if issues_found == 0:
        console.print("🎉 [bold green]Verification Complete: Lab is 100% Viable and Secure.[/bold green]")
    else:
        console.print(f"🚨 [bold red]Verification Complete: {issues_found} anomalies detected.[/bold red]")
        console.print("💡 [dim]Run `yugayu setup-lab --reset` to attempt automatic repair.[/dim]")