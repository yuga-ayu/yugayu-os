import os
import subprocess
from pathlib import Path
from rich.console import Console
from yugayu.core.state.ledger_manager import load_config
from yugayu.core.logger import log_command
from yugayu.core.economy.treasury_wallet import process_transaction

console = Console()

def generate_image(ayu_name: str, prompt: str, output_path: str, input_image: str = None) -> bool:
    """Agnostic execution: Fires the command defined in the entity's ledger."""
    config = load_config()
    lab_root = Path(config.lab_root).expanduser()
    
    ayu_entry = next((a for a in config.ayus if a.name == ayu_name), None)
    if not ayu_entry or not ayu_entry.inference_command:
        console.print(f"❌ [red]Entity {ayu_name} lacks an inference_command.[/red]")
        return False

    ayu_dir = lab_root / "ayus" / ayu_name
    output_dir = ayu_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    final_output_file = output_dir / Path(output_path).name
    
    if not process_transaction(ayu_name, 1.0, "execution_start"):
        console.print("❌ [red]Insufficient Prana. Execution blocked.[/red]")
        return False

    # Safely inject the prompt and optional input image
    safe_prompt = prompt.replace("'", "'\\''")
    exec_cmd = ayu_entry.inference_command.replace("{prompt}", safe_prompt).replace("{output}", str(final_output_file))
    
    if input_image:
        exec_cmd = exec_cmd.replace("{input}", f"--input '{input_image}'")
    else:
        exec_cmd = exec_cmd.replace("{input}", "") # Strip the tag if no image is provided

    console.print(f"🧠 [yellow]Karma Engine: Booting {ayu_name}...[/yellow]")
    console.print(f"⚙️  [cyan]Executing:[/cyan] [dim]{exec_cmd}[/dim]")
    console.print("🔒 [green]Telemetry Blocked. Operating locally.[/green]")
    
    secure_env = os.environ.copy()
    secure_env["HF_HUB_OFFLINE"] = "1"
    secure_env["DISABLE_TELEMETRY"] = "1"
    
    try:
        result = subprocess.run(exec_cmd, shell=True, cwd=str(ayu_dir), env=secure_env)
        
        if result.returncode != 0:
            console.print(f"❌ [bold red]Execution failed with exit code {result.returncode}[/bold red]")
            log_command(f"ask {ayu_name} '{prompt}'", status="FAILED")
            return False
            
        console.print(f"🎉 [bold green]Task complete. Artifact secured at {final_output_file}[/bold green]")
        process_transaction(ayu_name, 1.0, "execution_success")
        log_command(f"ask {ayu_name} '{prompt}'", status="SUCCESS")
        return True
        
    except Exception as e:
        console.print(f"❌ [bold red]Engine Failure: {e}[/bold red]")
        log_command(f"ask {ayu_name} '{prompt}'", status="FAILED")
        return False