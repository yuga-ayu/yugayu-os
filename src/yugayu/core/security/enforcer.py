from pathlib import Path
from rich.console import Console
from yugayu.core.state.ledger_manager import load_config, save_config

console = Console()

def quarantine_entity(entity_id: str, reason: str):
    """
    [Enforcer Department]
    Flags an entity as quarantined in the immutable ledger.
    """
    console.print(f"🚨 [bold red]ENFORCER: Quarantining entity '{entity_id}'[/bold red]")
    console.print(f"Reason: {reason}")
    
    config = load_config()
    entity_found = False
    
    for ayu in config.ayus:
        if ayu.name == entity_id:
            ayu.status = "quarantined"
            entity_found = True
            break
            
    if entity_found:
        save_config(config)
        console.print(f"🔒 [red]Ledger Updated: {entity_id} is permanently locked.[/red]")
    else:
        # If it's not an Ayu, it might be an unauthorized external actor.
        console.print("⚠️ [yellow]Threat logged. Origin entity not found in local ledger.[/yellow]")