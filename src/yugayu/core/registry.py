"""
Central Registry for Yugayu CLI Commands.
Statuses: 'active', 'deprecated', 'blacklisted'
"""

COMMAND_REGISTRY = {
    "init":   {"module": "init",   "status": "active"},
    "create": {"module": "create", "status": "active"},
    "info":   {"module": "info",   "status": "active"},
    "log":    {"module": "log",    "status": "active"}
}