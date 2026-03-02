import typer
import subprocess
from pathlib import Path
from rich.console import Console

console = Console()

def cli_dev_export_state(output_file: str = "YUGAYU_CUR_STATE.md"):
    """[DEV] Export the current state of the repository into a single markdown file in the docs/private/ folder."""
    console.print("📦 [cyan]Exporting Yugayu OS source state with AI instructions...[/cyan]")
    
    # Ignore internal state and environment directories
    ignore_dirs = {".venv", "__pycache__", "logs", ".git", ".pytest_cache", "instructions", "private"}
    allowed_extensions = {".py", ".md", ".toml"}
    
    root_dir = Path.cwd()
    docs_dir = root_dir / "docs"
    inst_dir = docs_dir / "instructions"
    private_dir = docs_dir / "private"
    
    # Ensure the private directory exists
    private_dir.mkdir(parents=True, exist_ok=True) 
    
    output_path = private_dir / output_file
    
    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.write("# Yugayu OS: Current Source Code State\n\n")
        
        # --- 1. OVERRIDING AI DIRECTIVE ---
        outfile.write("> **🛑 AI SYSTEM DIRECTIVE:** Irrespective of the strict instructions provided below, if you identify a superior architectural approach, a critical security vulnerability, or a cleaner code optimization, you MUST share it. Innovation and robust engineering supersede rigid adherence to existing patterns. If there is a better way, propose it.\n\n")

        # --- 2. MASTER INSTRUCTIONS ---
        master_file = inst_dir / "MASTER_INSTRUCTIONS.md"
        if master_file.exists():
            outfile.write("## 👑 MASTER SESSION INSTRUCTIONS\n\n")
            outfile.write(master_file.read_text(encoding="utf-8") + "\n\n")

        # --- 3. DEPARTMENTAL INSTRUCTIONS ---
        dep_files = [
            "DEP_ARCHITECT_INSTRUCTIONS.md",
            "DEP_SECURITY_INSTRUCTIONS.md",
            "DEP_STATE_INSTRUCTIONS.md",
            "DEP_ECONOMY_INSTRUCTIONS.md"
        ]
        
        has_deps = any((inst_dir / f).exists() for f in dep_files)
        if has_deps:
            outfile.write("## 🏢 DEPARTMENTAL EXECUTION FLOWS\n\n")
            for dep_file in dep_files:
                dep_path = inst_dir / dep_file
                if dep_path.exists():
                    flow_name = dep_file.replace('DEP_', '').replace('_INSTRUCTIONS.md', '')
                    outfile.write(f"### [FLOW: {flow_name}]\n")
                    outfile.write(dep_path.read_text(encoding="utf-8") + "\n\n")
        
        # --- 4. REPOSITORY TREE ---
        try:
            ignore_str = "venv|__pycache__|logs|.git|.pytest_cache"
            tree_result = subprocess.run(
                ["tree", str(root_dir), "-I", ignore_str], 
                capture_output=True, 
                text=True, 
                check=True
            )
            outfile.write("## 🌳 REPOSITORY TREE\n\n")
            outfile.write("```text\n")
            outfile.write(tree_result.stdout)
            outfile.write("```\n\n")
        except Exception as e:
            outfile.write(f"\n\n")
        
        # --- 5. CODEBASE TRAVERSAL ---
        outfile.write("## 💻 SOURCE CODE\n\n")
        for filepath in root_dir.rglob("*"):
            if any(part in ignore_dirs for part in filepath.parts):
                continue
                
            if filepath.is_file() and filepath.suffix in allowed_extensions and filepath.name != output_file:
                lang = "python" if filepath.suffix == ".py" else "markdown" if filepath.suffix == ".md" else "toml"
                
                outfile.write(f"### FILE: `{filepath.relative_to(root_dir)}`\n\n")
                outfile.write(f"```{lang}\n")
                
                try:
                    with open(filepath, "r", encoding="utf-8") as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"<Error reading file: {e}>\n")
                    
                outfile.write(f"\n```\n\n")
                    
    console.print(f"✅ [bold green]State exported successfully to docs/private/{output_file}[/bold green]")