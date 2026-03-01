import os
from functools import wraps
from rich.console import Console
from pathlib import Path
from yugayu.core.security.identity_verifier import Ed25519Bouncer

console = Console()

def yugayu_router(func):
    """Strict Zero-Trust Middleware router for ALL CLI commands."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        # 1. Genesis Exception: Only the setup command can run without prior identity
        if func.__name__ == "cli_setup_lab":
            return func(*args, **kwargs)
            
        admin_id = "admin-cli"
        config_dir = Path.home() / ".yugayu"
        admin_wallet_path = config_dir / "admin-identity.json"
        
        # 2. Strict Check: If no identity exists, block execution completely.
        if not admin_wallet_path.exists():
            console.print("❌ [bold red]SYSTEM OFFLINE: Local Admin Identity not found.[/bold red]")
            console.print(f"💡 [yellow]Run `yugayu setup-lab` to provision your cryptographic passport in {config_dir}.[/yellow]")
            return None
                
        # 3. Strict Verification: Every command goes through the bouncer
        bouncer = Ed25519Bouncer()
        
        # MVP: Simulating the signed payload validation
        if bouncer.verify_identity(admin_id, b"cli_payload", b"simulated_signature", custom_path=admin_wallet_path):
            return func(*args, **kwargs)
        else:
            console.print("[red]Access Denied by Identity Verifier.[/red]")
            return None
            
    return wrapper