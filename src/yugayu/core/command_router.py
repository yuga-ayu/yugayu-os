from functools import wraps
from rich.console import Console
from yugayu.core.iam_bouncer import Ed25519Bouncer

console = Console()

def yugayu_router(func):
    """
    The central routing decorator for Yugayu CLI commands.
    It intercepts the command, checks the IAM Bouncer, and routes execution.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # We extract the ayu_name if it is passed to the CLI command
        ayu_name = kwargs.get("ayu_name")
        
        # If the command targets a specific Ayu, it must pass the IAM Bouncer
        if ayu_name:
            bouncer = Ed25519Bouncer()
            # We use dummy payload/signature bytes for now until the wallet is fully implemented
            if not bouncer.verify_identity(ayu_name, payload=b"dummy", signature=b"dummy"):
                console.print(f"[bold red]❌ AuthError: IAM Bouncer blocked execution for {ayu_name}.[/bold red]")
                return None
                
        return func(*args, **kwargs)
    return wrapper