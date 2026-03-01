import sys
from rich.console import Console
from yugayu.core.state.ledger_manager import load_config
from yugayu.core.logger import log_command, log_error

console = Console()

def cli_status():
    """Show current lab status."""
    full_cmd = " ".join(sys.argv)
    
    try:
        cfg = load_config()
        console.print(f"[bold]Lab Root:[/bold] {cfg.lab_root}")
        console.print(f"[bold]ayus:[/bold] {len(cfg.ayus)}")
        
        if cfg.ayus:
            console.print("\n[bold]Active ayus:[/bold]")
            for p in cfg.ayus:
                console.print(f"  - [cyan]{p.name}[/cyan] ({p.status})")
                
        if cfg.nas_path:
            console.print(f"\n[bold]NAS Backup:[/bold] {cfg.nas_path}")
            
        log_command(full_cmd)
    except Exception as e:
        log_error(full_cmd, str(e))
