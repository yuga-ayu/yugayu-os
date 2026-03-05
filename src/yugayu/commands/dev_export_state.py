import typer
import subprocess
import ast
from pathlib import Path
from rich.console import Console

console = Console()

def get_yugayu_imports(filepath: Path, repo_root: Path) -> set[Path]:
    """Parses a Python file using AST to find all internal yugayu.* imports."""
    deps = set()
    if not filepath.exists() or filepath.suffix != ".py":
        return deps
    
    try:
        tree = ast.parse(filepath.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith("yugayu"):
                    for alias in node.names:
                        parts = node.module.split('.') + [alias.name]
                        abs_path = repo_root / "src" / Path(*parts).with_suffix(".py")
                        if abs_path.exists(): deps.add(abs_path)
                        else:
                            parts_mod = node.module.split('.')
                            abs_path_mod = repo_root / "src" / Path(*parts_mod).with_suffix(".py")
                            if abs_path_mod.exists(): deps.add(abs_path_mod)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith("yugayu"):
                        parts = alias.name.split('.')
                        abs_path = repo_root / "src" / Path(*parts).with_suffix(".py")
                        if abs_path.exists(): deps.add(abs_path)
    except Exception:
        pass
    return deps

def resolve_dependencies(start_file: Path, repo_root: Path) -> set[Path]:
    resolved = {start_file}
    queue = [start_file]
    while queue:
        current = queue.pop(0)
        new_deps = get_yugayu_imports(current, repo_root)
        for dep in new_deps:
            if dep not in resolved:
                resolved.add(dep)
                queue.append(dep)
    return resolved

def cli_dev_export_state(
    output_file: str = typer.Option("YUGAYU_CUR_STATE.md", "--output", "-o", help="Output file name"),
    include_lab: bool = typer.Option(False, "--include-lab", "-ilab", help="Include physical lab tree"),
    no_tree: bool = typer.Option(False, "--no-tree", help="Skip the repository tree output"),
    include_tests: bool = typer.Option(False, "--include-tests", "-itests", help="Include all test files in the export"),
    command: str = typer.Option(None, "--command", "-c", help="Export ONLY a specific command and its dependencies"),
    test_name: str = typer.Option(None, "--test", "-t", help="Export ONLY a specific test and its dependencies")
):
    """[DEV] Export the repository state. Default: Core .py files + Repo Tree."""
    from yugayu.core.state.ledger_manager import load_config
    
    console.print("📦 [cyan]Exporting Yugayu OS source state...[/cyan]")
    
    config = load_config()
    if not config.os_source_path or not Path(config.os_source_path).exists():
        console.print("❌ [red]Repository path not registered in Ledger. Run `setup-lab --reset` inside the repo.[/red]")
        return
        
    repo_root = Path(config.os_source_path)
    private_dir = repo_root / "docs" / "private"
    private_dir.mkdir(parents=True, exist_ok=True) 
    
    output_path = private_dir / output_file
    target_files = set()
    
    # 1. Dependency Resolution Mode (Command or Test)
    if command:
        cmd_module = command.replace("-", "_")
        start_file = repo_root / "src" / "yugayu" / "commands" / f"{cmd_module}.py"
        if start_file.exists():
            console.print(f"🔍 [dim]AST Parser: Tracing dependencies for command '{command}'...[/dim]")
            target_files.update(resolve_dependencies(start_file, repo_root))
        else:
            console.print(f"❌ [red]Command file not found: {start_file.name}[/red]")
            
    if test_name:
        test_file = next(repo_root.rglob(f"{test_name}.py"), None)
        if test_file:
            console.print(f"🔍 [dim]AST Parser: Tracing dependencies for test '{test_name}'...[/dim]")
            target_files.update(resolve_dependencies(test_file, repo_root))
        else:
            console.print(f"❌ [red]Test file not found: {test_name}.py[/red]")

    exported_file_count = 0

    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.write(f"# Yugayu OS: Current Source Code State\n\n")
        
        # 2. REPOSITORY TREE
        if not no_tree:
            try:
                ignore_str = "venv|.venv|__pycache__|logs|.git|.pytest_cache|instructions|private"
                tree_result = subprocess.run(["tree", str(repo_root), "-I", ignore_str], capture_output=True, text=True, check=True)
                outfile.write("## 🌳 REPOSITORY TREE\n\n```text\n")
                outfile.write(tree_result.stdout)
                outfile.write("```\n\n")
            except Exception: pass
            
        # 3. LAB TREE
        if include_lab:
            try:
                lab_root = Path(config.lab_root).expanduser()
                if lab_root.exists():
                    ignore_str_lab = "venv|.venv|__pycache__"
                    lab_tree = subprocess.run(["tree", str(lab_root), "-I", ignore_str_lab], capture_output=True, text=True, check=True)
                    outfile.write("## 🏗️ PHYSICAL LAB TREE\n\n```text\n")
                    outfile.write(lab_tree.stdout)
                    outfile.write("```\n\n")
            except Exception: pass

        # 4. CODEBASE TRAVERSAL
        outfile.write("## 💻 SOURCE CODE\n\n")
        
        ignore_dirs = {".venv", "venv", "__pycache__", "logs", ".git", ".pytest_cache", "private", "instructions"}
        
        if command or test_name:
            files_to_process = target_files
        else:
            files_to_process = []
            for f in repo_root.rglob("*.py"):
                if any(p in ignore_dirs for p in f.parts): continue
                # Default behavior: Skip tests unless explicitly included
                if "test" in f.parts and not include_tests: continue
                files_to_process.append(f)
                
        for filepath in files_to_process:
            if filepath.is_file() and filepath.suffix == ".py":
                exported_file_count += 1
                outfile.write(f"### FILE: `{filepath.relative_to(repo_root)}`\n\n")
                outfile.write(f"```python\n")
                try:
                    outfile.write(filepath.read_text(encoding="utf-8"))
                except Exception as e:
                    outfile.write(f"<Error reading file: {e}>\n")
                outfile.write(f"\n```\n\n")

    # --- 5. PRINT THE RECEIPT ---
    summary = ["\n[bold]📊 Export Summary:[/bold]"]
    
    if command:
        summary.append(f"  [dim]•[/dim] Target: Command [cyan]'{command}'[/cyan]")
    elif test_name:
        summary.append(f"  [dim]•[/dim] Target: Test [cyan]'{test_name}'[/cyan]")
    else:
        summary.append(f"  [dim]•[/dim] Target: [cyan]Full Codebase[/cyan]")

    summary.append(f"  [dim]•[/dim] Repo Tree: {'[dim]Excluded[/dim]' if no_tree else '[green]Included[/green]'}")
    summary.append(f"  [dim]•[/dim] Lab Tree: {'[green]Included[/green]' if include_lab else '[dim]Excluded[/dim]'}")
    
    if not (command or test_name):
        summary.append(f"  [dim]•[/dim] Tests: {'[green]Included[/green]' if include_tests else '[dim]Excluded[/dim]'}")
        
    summary.append(f"  [dim]•[/dim] Python Files Exported: [yellow]{exported_file_count}[/yellow]\n")

    console.print("\n".join(summary))
    console.print(f"✅ [bold green]State exported successfully to docs/private/{output_file}[/bold green]")