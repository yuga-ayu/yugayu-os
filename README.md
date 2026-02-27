# Yugayu AI Orchestration Protocol (Project Parvati)

![CI Status](https://github.com/yuga-ayu/yugayu-os/actions/workflows/ci.yml/badge.svg)
[![License: BSL](https://img.shields.io/badge/License-BSL-blue.svg)](./LICENSE)

**Yugayu OS** is a Distributed, Zero-Trust AI Operating System designed to decouple AI intent from hardware execution using Post-Quantum Cryptography (PQC).

Current AI infrastructure suffers from massive VRAM fragmentation, storage bloat, and insecure execution environments. Yugayu solves this by scaffolding isolated AI entities (ayus) across a trustless, multi-node network, utilizing cryptographic passports and a centralized immutable ledger.

## Core Architecture (v0.2.0)
* **Hot-Swappable E2E Transport:** Built on Python `typing.Protocol` to seamlessly integrate Kyber key encapsulation and AES-256-GCM encryption.
* **iam-bouncer:** Cryptographically signs and verifies API requests using local `.yugayu-identity` wallets. Fails closed.
* **state-management:** Handles the secure storage and rotation of keys, active sessions, and global lab configuration.
* **Prana Economy:** A closed-loop token system that rewards ayus for safe generations and quarantines them for malformed outputs.

## Installation & Quickstart

Yugayu uses `uv` for lightning-fast dependency management.

```bash
git clone [https://github.com/yuga-ayu/yugayu-os.git](https://github.com/yuga-ayu/yugayu-os.git)
cd yugayu-os
uv tool install -e .

yugayu setup_lab
yugayu create-ayu my-first-agent