import functools
from rich.console import Console
from yugayu.core.logger import check_log_size_warning

console = Console()

def yugayu_middleware(func):
    """
    A wrapper that runs automatically before every command.
    Checks logs, and acts as the future IAM Gatekeeper.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # PRE-FLIGHT CHECKS
        if check_log_size_warning():
            console.print("[bold red]⚠️ WARNING:[/bold red] [yellow]Logs exceed size limit. Please backup to NAS.[/yellow]\n")
            
        # EXECUTE THE ACTUAL COMMAND
        return func(*args, **kwargs)
        
    return wrapper