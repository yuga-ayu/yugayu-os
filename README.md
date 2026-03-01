# Yugayu AI Lab Orchestrator

![CI Status](https://github.com/yuga-ayu/yugayu-os/actions/workflows/ci.yml/badge.svg)
[![License: BSL](https://img.shields.io/badge/License-BSL-blue.svg)](./LICENSE)
[![Version: 0.3.0](https://img.shields.io/badge/Version-0.3.0-purple.svg)]()

Yugayu OS is a zero-trust, distributed AI operating system designed to orchestrate isolated AI entities across local, multi-node hardware environments. 

It decouples AI execution intent from hardware via Post-Quantum Cryptography (PQC) and mutual Merkle-tree authentication. By scaffolding isolated AI entities across a trustless network, Yugayu prevents VRAM fragmentation, storage bloat, and insecure execution, ensuring highly capable models (like FLUX.2) run securely in local-first, offline environments.

## Core Architecture
The system enforces strict separation between the **Control Plane** (`~/.yugayu`) and the **Physical Execution Lab** (`~/yugayu-lab`). It is divided into distinct, hot-swappable modules:

* **Security:** Handles PQC key encapsulation, AES-256-GCM transport, and strict asymmetric identity verification via the `iam-bouncer`. Fails closed.
* **Economy:** Manages a closed-loop Prana token system enforcing execution costs and hardware resource allocation based on entity reputation ("Honor Scores").
* **State (The Ledger):** Maintains an immutable Merkle-tree blockchain. Every entity, shared library, and execution engine possesses a cryptographic passport. 
* **Compliance:** Enforces boundary checks on open-source model licenses and strictly blocks external telemetry at the OS level.
* **Execution:** A dynamic capability registry that routes verified payloads to the appropriate local GPU hardware or vector database node.

## Installation
```bash
git clone [https://github.com/yuga-ayu/yugayu-os.git](https://github.com/yuga-ayu/yugayu-os.git)
cd yugayu-os
uv tool install -e .

# Bootstrap the Lab and provision the Admin Master Key
yugayu setup-lab

# Interactively scaffold a new AI entity
yugayu wakeup-ayu

# Query the cryptographic ledger
yugayu identify my-vision-agent