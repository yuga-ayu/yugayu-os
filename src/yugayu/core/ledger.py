# src/yugayu/core/ledger.py
import json
import hashlib
from pathlib import Path
from rich.console import Console

console = Console()
LEDGER_PATH = Path.home() / ".yugayu" / "ledger.json"

def _get_ledger() -> list:
    if not LEDGER_PATH.exists():
        # The Genesis Block
        return [{"index": 0, "previous_hash": "0" * 64, "payload": "GENESIS"}]
    with open(LEDGER_PATH, "r") as f:
        return json.load(f)

def verify_chain() -> bool:
    """Validates the Merkle chain. If tampered, the system locks down."""
    ledger = _get_ledger()
    for i in range(1, len(ledger)):
        prev_block = ledger[i-1]
        current_block = ledger[i]
        
        # Re-hash the previous block to ensure it matches the stored previous_hash
        block_string = json.dumps(prev_block, sort_keys=True).encode()
        expected_hash = hashlib.sha256(block_string).hexdigest()
        
        if current_block["previous_hash"] != expected_hash:
            console.print("[bold red]🚨 CRITICAL: Ledger tampering detected! System locked into Safe State.[/bold red]")
            return False
    return True

def record_transaction(ayu_id: str, command: str, status: str):
    """Writes a new execution block to the ledger."""
    ledger = _get_ledger()
    prev_block = ledger[-1]
    
    block_string = json.dumps(prev_block, sort_keys=True).encode()
    new_hash = hashlib.sha256(block_string).hexdigest()
    
    new_block = {
        "index": len(ledger),
        "previous_hash": new_hash,
        "ayu_id": ayu_id,
        "command": command,
        "status": status
    }
    
    ledger.append(new_block)
    
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LEDGER_PATH, "w") as f:
        json.dump(ledger, f, indent=4)