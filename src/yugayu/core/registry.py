"""
Central Registry for Yugayu CLI Commands.
Statuses: 'active', 'deprecated', 'blacklisted'
"""

COMMAND_REGISTRY = {
    # Core commands
    "setup-lab": {"module": "setup_lab", "status": "active", "env": "prod"},
    "wakeup-ayu": {"module": "wakeup_ayu", "status": "active", "env": "prod"},
    "ask": {"module": "ask", "status": "active", "env": "prod"},
    "identify": {"module": "identify", "status": "active", "env": "prod"},
    "status": {"module": "status", "status": "active", "env": "prod"},
    "activity": {"module": "activity", "status": "active", "env": "prod"},
    
    # Deprecated
    "init": {"module": "init", "status": "deprecated", "env": "prod"},

    # Developer commands
    "tree": {"module": "dev_tree", "status": "active", "env": "dev"},
    "run-test": {"module": "dev_run_test", "status": "active", "env": "dev"},
    "export-state": {"module": "dev_export_state", "status": "active", "env": "dev"}
}