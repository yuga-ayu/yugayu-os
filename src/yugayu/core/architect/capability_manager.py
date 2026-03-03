import os
import subprocess
import shlex
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from yugayu.core.state.ledger_manager import load_config, save_config, ayuModel, ayuEntry
from yugayu.core.security.identity_issuer import issue_identity

console = Console()

def provision_ayu_from_manifest(ayu_name: str, manifest_data: dict) -> bool:
    """[Architect Department] Orchestrates dynamic downloads, symlinks, and identity."""
    config = load_config()
    lab_root = Path(config.lab_root).expanduser()
    shared_models_dir = lab_root / "shared" / "models" / "base"
    private_ayu_dir = lab_root / "ayus" / ayu_name
    
    (private_ayu_dir / "models").mkdir(parents=True, exist_ok=True)
    (private_ayu_dir / "private_data").mkdir(parents=True, exist_ok=True)
    
    console.print(f"\n⚙️  [cyan]Architect: Analyzing capabilities for {ayu_name}...[/cyan]")
    
    # 1. Provision Cryptographic Identity for the Ayu
    wallet_path = private_ayu_dir / ".yugayu-identity"
    if not wallet_path.exists():
        console.print(f"🔑 [cyan]Minting Ed25519 Cryptographic Passport for {ayu_name}...[/cyan]")
        issue_identity(ayu_name, "ayu", custom_path=wallet_path)
    
    # 2. Process Resources dynamically
    resources = manifest_data.get("resources", [])
    
    for res in resources:
        res_name = res.get("name")
        is_shared = res.get("shareable", True)
        fetch_cmd_raw = res.get("fetch_command", "")
        
        # Format the paths
        fetch_cmd = fetch_cmd_raw.replace("{shared_dir}", str(shared_models_dir)).replace("{private_dir}", str(private_ayu_dir))
        
        target_path = shared_models_dir / res_name if is_shared else private_ayu_dir / "private_data" / res_name

        if not target_path.exists() and fetch_cmd:
            console.print(f"📥 [yellow]Resource missing: {res_name}.[/yellow]")
            consent = Prompt.ask(f"Execute fetch command? `[dim]{fetch_cmd}[/dim]`", choices=["Y", "N"], default="Y")
            
            if consent == "Y":
                console.print(f"⚙️  Executing: {fetch_cmd}")
                try:
                    # Execute the agnostic fetch command
                    subprocess.run(shlex.split(fetch_cmd), check=True)
                    if is_shared:
                        config.models.append(ayuModel(name=res_name, path=str(target_path)))
                except subprocess.CalledProcessError as e:
                    console.print(f"❌ [red]Fetch failed: {e}[/red]")
                    return False
            else:
                return False
                
        # Symlink shared resources
        if is_shared and target_path.exists():
            symlink_target = private_ayu_dir / "models" / res_name
            if not symlink_target.exists():
                console.print(f"🔗 [cyan]Symlinking {res_name} to Ayu environment...[/cyan]")
                try:
                    os.symlink(target_path, symlink_target)
                except FileExistsError:
                    pass

    # 3. Register the Ayu in the ledger with its execution command
    exec_cmd = manifest_data.get("execution", {}).get("inference_command", "")
    existing_ayu = next((a for a in config.ayus if a.name == ayu_name), None)
    
    if not existing_ayu:
        new_ayu = ayuEntry(name=ayu_name, path=str(private_ayu_dir), status="active", inference_command=exec_cmd)
        config.ayus.append(new_ayu)
    else:
        existing_ayu.inference_command = exec_cmd

    save_config(config)
    return True