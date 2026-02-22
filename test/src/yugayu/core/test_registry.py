from yugayu.core.registry import COMMAND_REGISTRY

def test_registry_structure():
    # Ensure every registered command has the required metadata fields
    for cmd_name, meta in COMMAND_REGISTRY.items():
        assert "module" in meta, f"Command '{cmd_name}' missing 'module'"
        assert "status" in meta, f"Command '{cmd_name}' missing 'status'"
        assert meta["status"] in ["active", "deprecated", "blacklisted"], \
            f"Invalid status for '{cmd_name}'"
