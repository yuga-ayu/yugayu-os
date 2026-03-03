# Yugayu AI Lab Orchestrator

![CI Status](https://github.com/yuga-ayu/yugayu-os/actions/workflows/ci.yml/badge.svg)
[![License: Dual](https://img.shields.io/badge/License-Dual_(Free_Non--Commercial)-blue.svg)](./LICENSE)
[![Version: 0.4.0](https://img.shields.io/badge/Version-0.4.0-purple.svg)]()

Yugayu OS is a zero-trust, distributed AI operating system designed to orchestrate isolated AI entities across local, multi-node hardware environments. 

It decouples AI execution intent from hardware via Post-Quantum Cryptography (PQC) and mutual Merkle-tree authentication. By scaffolding isolated AI entities across a trustless network, Yugayu prevents VRAM fragmentation, storage bloat, and insecure execution, ensuring highly capable models (like FLUX.2) run securely in local-first, offline environments.

## Core Architecture
The system enforces strict separation between the **Control Plane** (`~/.yugayu`) and the **Physical Execution Lab** (`~/yugayu-lab`).

* **Security:** PQC PQC key encapsulation, AES-256-GCM transport, and strict asymmetric identity verification (`iam-bouncer`).
* **Economy (Prana):** Flat-rate token escrow system enforcing execution execution costs and hardware resource allocation.
* **State (The Ledger):** Maintains an immutable blockchain log. Every entity possesses a cryptographic passport. 
* **Compliance (Dharma Warden):** Mathematically enforces boundary checks on open-source model licenses (e.g., BSL) and strictly blocks external telemetry via OS-level environment routing.
* **Execution (Symlink Web):** A dynamic capability registry that routes verified prompts to private entity folders, tricking inference libraries into loading multi-gigabyte models from a single, centralized shared plane.

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