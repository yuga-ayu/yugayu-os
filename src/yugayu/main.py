import typer
import importlib
from rich.console import Console
from yugayu.core.registry import COMMAND_REGISTRY
from yugayu.core.utils import yugayu_middleware

app = typer.Typer(help="Yugayu AI Lab Orchestrator")
console = Console()

# Iterate through our central registry dynamically
for cmd_name, meta in COMMAND_REGISTRY.items():
    
    if meta["status"] == "blacklisted":
        continue
        
    try:
        # Dynamically load the python file
        module_path = f"yugayu.commands.{meta['module']}"
        module = importlib.import_module(module_path)
        
        # Grab the target function
        func_name = f"cli_{meta['module']}"
        func = getattr(module, func_name)
        
        # Wrap the function with our pre-flight checks and middleware
        wrapped_func = yugayu_middleware(func)
        
        # Attach to the CLI interface
        is_deprecated = (meta["status"] == "deprecated")
        app.command(name=cmd_name, deprecated=is_deprecated)(wrapped_func)
        
    except ImportError as e:
        console.print(f"[red]Error loading command '{cmd_name}': Module not found. ({e})[/red]")
    except AttributeError:
        console.print(f"[red]Error loading command '{cmd_name}': Function '{func_name}' not found.[/red]")

if __name__ == "__main__":
    app()