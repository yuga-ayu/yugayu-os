# TODO: [SECURITY] IAM Gatekeeper: Intercept command, verify cryptographic signature from Ayu's wallet before execution.
# TODO: [TRACKING] Token/Compute Usage: Intercept API payloads to ComfyUI/vLLM, calculate token/VRAM usage, and write to ledger.
# TODO: [MONETIZATION] Link token usage to Honor Score (higher score = lower compute cost/priority queuing).

import functools
from rich.console import Console
from yugayu.core.logger import check_log_size_warning
from yugayu.core.iam import verify_identity
from yugayu.core.ledger import verify_chain, record_transaction

console = Console()

def yugayu_gateway(func):
    """
    A wrapper that runs automatically before every command.
    Checks logs, verifies blockchain integrity, and acts as the IAM Gatekeeper.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        command_name = func.__name__
        
        # 1. LEDGER INTEGRITY CHECK (Zero Trust Prevention)
        if not verify_chain():
            return None # Blocks command immediately
        
        # 2. IAM SECURITY CHECK
        # Extract ayu_id if provided, otherwise assume it's a root system command
        ayu_id = kwargs.get('ayu_name', 'system_admin') 
        
        if ayu_id != 'system_admin' and not verify_identity(ayu_id, payload=command_name):
            console.print(f"[bold red]❌ AuthError:[/bold red] [red]Invalid signature for Ayu: {ayu_id}.[/red]")
            record_transaction(ayu_id, command_name, "DENIED_AUTH")
            return None 
            
        # 3. PRE-FLIGHT MAINTENANCE CHECKS
        if check_log_size_warning():
            console.print("[bold red]⚠️ WARNING:[/bold red] [yellow]Logs exceed size limit. Please backup to NAS.[/yellow]\n")
            
        # 4. EXECUTE THE ACTUAL COMMAND
        result = func(*args, **kwargs)
        
        # 5. COMMIT TO LEDGER
        record_transaction(ayu_id, command_name, "SUCCESS")
        
        return result
        
    return wrapper
