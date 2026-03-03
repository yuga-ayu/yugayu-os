from rich.console import Console

console = Console()

# MVP Hardcoded acceptable licenses
VALID_LICENSES = ["bsl-non-commercial", "mit", "apache-2.0", "openrail"]

def verify_license_compliance(manifest_data: dict) -> bool:
    """Ensures the entity has explicitly agreed to the underlying model's license."""
    entity = manifest_data.get("entity", {})
    accepted = entity.get("license_accepted", "").lower()
    
    console.print("⚖️  [yellow]Dharma Warden: Auditing license compliance...[/yellow]")
    
    if accepted not in VALID_LICENSES:
        console.print(f"❌ [red]Compliance Failure: Unrecognized or missing license agreement ('{accepted}').[/red]")
        return False
        
    console.print(f"✅ [green]Compliance Passed: Operating under '{accepted}'.[/green]")
    return True