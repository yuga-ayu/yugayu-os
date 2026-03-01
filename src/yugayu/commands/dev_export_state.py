import typer
from pathlib import Path
from rich.console import Console

console = Console()

def cli_dev_export_state(output_file: str = "YUGAYU_CUR_STATE.md"):
    """[DEV] Export the current state of the repository into a single markdown file in the docs/ folder."""
    console.print("📦 [cyan]Exporting Yugayu OS source state...[/cyan]")
    
    ignore_dirs = {".venv", "__pycache__", "logs", ".git", ".pytest_cache"}
    allowed_extensions = {".py", ".md", ".toml"}
    
    root_dir = Path.cwd()
    docs_dir = root_dir / "docs"
    docs_dir.mkdir(exist_ok=True) # Ensure docs folder exists
    
    output_path = docs_dir / output_file
    
    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.write("# Yugayu OS: Current Source Code State\n\n")
        
        # Traverse the directory tree
        for filepath in root_dir.rglob("*"):
            # Skip ignored directories
            if any(part in ignore_dirs for part in filepath.parts):
                continue
                
            # Only append allowed file types (and don't export the export file itself)
            if filepath.is_file() and filepath.suffix in allowed_extensions and filepath.name != output_file:
                
                # Determine syntax highlighting language
                lang = "python" if filepath.suffix == ".py" else "markdown" if filepath.suffix == ".md" else "toml"
                
                outfile.write(f"\n## FILE: `{filepath.relative_to(root_dir)}`\n\n")
                outfile.write(f"```{lang}\n")
                
                try:
                    with open(filepath, "r", encoding="utf-8") as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"<Error reading file: {e}>\n")
                    
                outfile.write(f"\n```\n")
                    
    console.print(f"✅ [bold green]State exported successfully to docs/{output_file}[/bold green]")