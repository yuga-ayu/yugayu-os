import typer
import importlib
import os
import json
import shlex
import sys
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

def setup_shell_autocomplete():
    """Wires up Unix readline to provide Tab completion for Yugayu commands."""
    try:
        import readline
        
        available_cmds = ["exit", "quit", "clear"]
        for cmd, meta in COMMAND_REGISTRY.items():
            if meta.get("status") != "blacklisted" and not meta.get("hidden"):
                available_cmds.append(cmd)
                
        def completer(text, state):
            options = [cmd for cmd in available_cmds if cmd.startswith(text)]
            if state < len(options):
                return options[state]
            return None
            
        readline.set_completer(completer)
        readline.parse_and_bind("tab: complete")
    except ImportError:
        pass

@app.command(name="shell", help="Enter the interactive Yugayu OS CLI shell.")
def cli_shell():
    """Start an interactive REPL session."""
    setup_shell_autocomplete()
    
    console.print("[bold cyan]🧬 Welcome to the Yugayu OS Shell. Type 'exit' to leave.[/bold cyan]")
    while True:
        try:
            cmd_str = input("yugayu> ").strip()
            if not cmd_str:
                continue
                
            if cmd_str.lower() in ["exit", "quit"]:
                console.print("[dim]Disconnecting from Yugayu OS...[/dim]")
                sys.exit(0)  # Explicitly kill the Python process, returning to Zsh
                
            elif cmd_str.lower() == "clear":
                import os
                os.system('clear' if os.name == 'posix' else 'cls')
                continue
                
            try:
                args = shlex.split(cmd_str)
            except ValueError as e:
                console.print(f"❌ [bold red]Syntax Error: {e}[/bold red]")
                continue
                
            try:
                app(args, standalone_mode=False)
            except SystemExit:
                pass  
            except Exception as e:
                console.print(f"❌ [bold red]Execution Error: {e}[/bold red]")
                
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Disconnecting from Yugayu OS...[/dim]")
            sys.exit(0)  # Handle Ctrl+C or Ctrl+D safely

@app.callback(invoke_without_command=True)
def default_behavior(ctx: typer.Context):
    """Intercept empty commands and launch the interactive shell."""
    if ctx.invoked_subcommand is None:
        cli_shell()

if __name__ == "__main__":
    app()