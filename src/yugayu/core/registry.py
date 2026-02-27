"""
Central Registry for Yugayu CLI Commands.
Statuses: 'active', 'deprecated', 'blacklisted'
"""

COMMAND_REGISTRY = {
    "setup-lab":  {"module": "setup_lab",  "status": "active"},
    "create-ayu": {"module": "create_ayu", "status": "active"},
    "activity":   {"module": "activity",   "status": "active"},
    "status":    {"module": "status",    "status": "active"},
    "tree": {"module": "tree", "status": "active"}
}
