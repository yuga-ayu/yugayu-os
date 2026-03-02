import typer
import importlib
import os
import json
from pathlib import Path
from rich.console import Console
from yugayu.core.registry import COMMAND_REGISTRY
from yugayu.core.command_router import yugayu_router
from yugayu.core.state.ledger_manager import load_config

app = typer.Typer(help="Yugayu AI Lab Orchestrator")
console = Console()

def check_maintainer_privilege() -> bool:
    """Passively reads the local identity to check if the user has developer clearance."""
    if os.environ.get("YUGAYU_DEV") == "1":
        return True
        
    admin_wallet_path = Path.home() / ".yugayu" / "admin-identity.json"
    if not admin_wallet_path.exists():
        return False
        
    try:
        with open(admin_wallet_path, "r") as f:
            wallet = json.load(f)
        config = load_config()
        
        # Maintainers get dev commands globally
        if wallet.get("role") == "maintainer" or wallet.get("entity_id") in config.admin_identities:
            return True
    except Exception:
        pass
        
    return False

is_dev_mode = check_maintainer_privilege()

for cmd_name, meta in COMMAND_REGISTRY.items():
    if meta["status"] == "blacklisted":
        continue
        
    if meta.get("env") == "dev" and not is_dev_mode:
        continue
        
    try:
        module_path = f"yugayu.commands.{meta['module']}"
        module = importlib.import_module(module_path)
        func_name = f"cli_{meta['module']}"
        func = getattr(module, func_name)
        
        wrapped_func = yugayu_router(func)
        is_deprecated = (meta["status"] == "deprecated")
        
        app.command(name=cmd_name, deprecated=is_deprecated)(wrapped_func)
        
    except ImportError as e:
        if is_dev_mode:
            console.print(f"[red]Dev Warning: Module '{cmd_name}' not found. ({e})[/red]")
    except AttributeError:
        if is_dev_mode:
            console.print(f"[red]Dev Warning: Function '{func_name}' not found for '{cmd_name}'.[/red]")

if __name__ == "__main__":
    app()