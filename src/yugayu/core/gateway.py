import functools
from rich.console import Console
from yugayu.core.logger import check_log_size_warning
from yugayu.core.iam import verify_identity

# TODO: [SECURITY] IAM Gatekeeper: Intercept command, verify cryptographic signature from Ayu's wallet before execution.
# TODO: [TRACKING] Token/Compute Usage: Intercept API payloads to ComfyUI/vLLM, calculate token/VRAM usage, and write to ledger.
# TODO: [MONETIZATION] Link token usage to Honor Score (higher score = lower compute cost/priority queuing).

console = Console()

def yugayu_gateway(func):
    """
    A wrapper that runs automatically before every command.
    Checks logs, and acts as the IAM Gatekeeper.
    """
    # TODO: [SECURITY] IAM Gatekeeper: Intercept command, verify cryptographic signature from Ayu's wallet before execution.
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        
        # 1. IAM SECURITY CHECK
        if not verify_identity():
            console.print("[bold red]❌ AuthError:[/bold red] [red]Invalid or quarantined Ayu identity token.[/red]")
            return None # Blocks the command from running
            
        # 2. PRE-FLIGHT MAINTENANCE CHECKS
        if check_log_size_warning():
            console.print("[bold red]⚠️ WARNING:[/bold red] [yellow]Logs exceed size limit. Please backup to NAS.[/yellow]\n")
            
        # 3. EXECUTE THE ACTUAL COMMAND
        return func(*args, **kwargs)
        
    return wrapper
