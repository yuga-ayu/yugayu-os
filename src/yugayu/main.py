import typer
import importlib
import os
from pathlib import Path
from rich.console import Console
from yugayu.core.registry import COMMAND_REGISTRY
from yugayu.core.command_router import yugayu_router

app = typer.Typer(help="Yugayu AI Lab Orchestrator")
console = Console()

# Auto-detect developer mode if running from source (.git exists)
is_dev_mode = Path(".git").exists() or os.environ.get("YUGAYU_DEV") == "1"

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
        # Silently skip incomplete MVP commands during testing unless in dev mode
        if is_dev_mode:
            console.print(f"[red]Dev Warning: Module '{cmd_name}' not found. ({e})[/red]")
    except AttributeError:
        if is_dev_mode:
            console.print(f"[red]Dev Warning: Function '{func_name}' not found for '{cmd_name}'.[/red]")

if __name__ == "__main__":
    app()