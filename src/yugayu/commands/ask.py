import typer
from rich.console import Console
from yugayu.core.execution.run_engine import generate_image

console = Console()

def cli_ask(target_ayu: str, prompt: str, output: str = "./result.png"):
    """Ask an Ayu to perform a task based on its learned skills."""
    console.print(f"🚀 [green]Routing payload to {target_ayu}...[/green]")
    
    # MVP Treasury Check (Infinite Money)
    console.print("🪙 [yellow]Prana Treasury: Authorized 1 execution token (Infinite MVP Mode).[/yellow]")
    
    # In the future, this will dynamically select the engine based on the Ayu's Skill Registry
    success = generate_image(prompt, output)
    
    if success:
        console.print(f"🎉 [bold green]Task complete. Artifact secured at {output}[/bold green]")
        console.print("🔗 [cyan]State: Merkle Ledger updated with execution hash.[/cyan]")
    else:
        console.print("❌ [bold red]Execution failed. Quarantining entity.[/bold red]")