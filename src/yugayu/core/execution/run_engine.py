import os
import subprocess
import shlex
from pathlib import Path
from rich.console import Console
from yugayu.core.state.ledger_manager import load_config
from yugayu.core.logger import log_command

os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["DISABLE_TELEMETRY"] = "1"

console = Console()

def generate_image(ayu_name: str, prompt: str, output_path: str) -> bool:
    """Agnostic Run Engine: Executes the command defined in the Ayu's ledger manifest."""
    config = load_config()
    lab_root = Path(config.lab_root).expanduser()
    
    # 1. Fetch Ayu Context
    ayu_entry = next((a for a in config.ayus if a.name == ayu_name), None)
    if not ayu_entry:
        console.print(f"❌ [red]Entity {ayu_name} not found in Ledger.[/red]")
        return False
        
    if not ayu_entry.inference_command:
        console.print(f"❌ [red]Entity {ayu_name} has no inference_command defined.[/red]")
        return False

    ayu_dir = lab_root / "ayus" / ayu_name
    output_dir = ayu_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    final_output_file = output_dir / Path(output_path).name
    
    # 2. Format the Command
    # Replace the {prompt} and {output} variables from the YAML with the actual CLI args
    raw_cmd = ayu_entry.inference_command
    exec_cmd = raw_cmd.replace("{prompt}", prompt).replace("{output}", str(final_output_file))

    console.print(f"🧠 [yellow]Karma Engine: Booting {ayu_name}...[/yellow]")
    console.print(f"⚙️  [cyan]Executing Agnostic Workload:[/cyan] [dim]{exec_cmd}[/dim]")
    
    # 3. Isolated Subprocess Execution
    try:
        # We run the command with `cwd=ayu_dir` so the script executes inside the isolated enclave
        result = subprocess.run(
            shlex.split(exec_cmd), 
            cwd=str(ayu_dir), 
            capture_output=True, 
            text=True
        )
        
        if result.returncode != 0:
            console.print(f"❌ [red]Execution Error:[/red]\n{result.stderr}")
            log_command(f"ask {ayu_name} '{prompt}'", status="FAILED")
            return False
            
        console.print(f"🎉 [bold green]Task complete. Artifact secured at {final_output_file}[/bold green]")
        log_command(f"ask {ayu_name} '{prompt}'", status="SUCCESS")
        return True
        
    except Exception as e:
        console.print(f"❌ [bold red]Engine Failure: {e}[/bold red]")
        log_command(f"ask {ayu_name} '{prompt}'", status="FAILED")
        return False