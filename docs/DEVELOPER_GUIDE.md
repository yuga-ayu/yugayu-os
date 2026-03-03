# Yugayu OS: Developer & Architecture Guide

Welcome to the Yugayu OS core repository. As a foundational Zero-Trust AI Operating System, we maintain high standards for code quality, security, and architectural consistency.

## System Architecture

Yugayu is divided into two strict planes, isolated by the **Command Router Middleware**:
1. **The Control Plane (`~/.yugayu`):** The absolute source of truth. It contains the Immutable Merkle Ledger (`config.yaml`), the Cryptographic Identity Keystore, and the Daily Execution Audit Logs. It contains no heavy weights.
2. **The Physical Lab (`~/yugayu-lab`):** The hardware abstraction layer containing the isolated AI workspaces, shared datasets, and multi-gigabyte Tensor weights.

### The Zero-Trust Execution Flow
No command executes directly on the host hardware. When a system or user triggers an action:
1. **Entry:** The CLI parses the requested command payload.
2. **Middleware:** The `@yugayu_router` intercepts the call before execution.
3. **RBAC Validation:** The router extracts the active Identity Role (`maintainer`, `admin`, `guest`).
4. **Cryptographic Bouncer:** The `Ed25519Bouncer` mathematically verifies the command payload against the entity's private key.
5. **The Enforcer Protocol:** If verification fails, the request is not just blocked; the `Enforcer` logs the violation to the ledger and the entity is permanently quarantined.

## Local Development Setup

Because Yugayu enforces Role-Based Access Control, you cannot access developer commands (like `tree` or `run-test`) without a valid `maintainer` identity. 

The OS uses a hardware-level check to determine your installation path. To attain `maintainer` clearance, you must install the OS in editable mode (`-e`) from a cloned git repository.

```bash
# 1. Clone the repository
git clone [https://github.com/yuga-ayu/yugayu-os.git](https://github.com/yuga-ayu/yugayu-os.git)
cd yugayu-os

# 2. Install in editable mode
uv tool install -e .

# 3. Bootstrap the lab and register the OS source path to the Ledger
yugayu setup-lab --reset

# 4. Verify your maintainer access and global diagnostic execution
yugayu run-test