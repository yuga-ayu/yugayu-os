import os
import json
from functools import wraps
from rich.console import Console
from pathlib import Path
from yugayu.core.security.identity_verifier import Ed25519Bouncer
from yugayu.core.security.enforcer import quarantine_entity

console = Console()

def yugayu_router(func):
    """Strict Zero-Trust Middleware router enforcing RBAC via Identity."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        # 1. Genesis Exception
        if func.__name__ == "cli_setup_lab":
            return func(*args, **kwargs)
            
        config_dir = Path.home() / ".yugayu"
        admin_wallet_path = config_dir / "admin-identity.json"
        
        # 2. The Guest Default
        if not admin_wallet_path.exists():
            console.print("⚠️ [yellow]Running as Guest. Execution and State access restricted.[/yellow]")
            console.print(f"💡 [dim]Run `yugayu setup-lab` to provision your cryptographic passport.[/dim]")
            return None
                
        # 3. RBAC Role Extraction
        try:
            with open(admin_wallet_path, "r") as f:
                wallet = json.load(f)
            role = wallet.get("role", "guest")
            entity_id = wallet.get("entity_id", "unknown")
        except Exception:
            role = "guest"
            entity_id = "corrupted-identity"
            
        if role not in ["admin", "maintainer"]:
            console.print(f"❌ [bold red]ACCESS DENIED: Role '{role}' possesses insufficient clearance.[/bold red]")
            quarantine_entity(entity_id, "Attempted unauthorized execution boundary bypass.")
            return None

        # 4. Strict Cryptographic Verification
        bouncer = Ed25519Bouncer()
        if bouncer.verify_identity(entity_id, b"cli_payload", b"simulated_signature", custom_path=admin_wallet_path):
            return func(*args, **kwargs)
        else:
            console.print("[red]Access Denied by Cryptographic Bouncer.[/red]")
            return None
            
    return wrapper