# Yugayu AI Orchestration Protocol (Project Parvati)

![CI Status](https://github.com/yuga-ayu/yugayu-os/actions/workflows/ci.yml/badge.svg)
[![License: BSL](https://img.shields.io/badge/License-BSL-blue.svg)](./LICENSE)

**Yugayu OS** is a Distributed, Zero-Trust AI Operating System designed to decouple AI intent from hardware execution. 

Current AI infrastructure suffers from massive VRAM fragmentation, storage bloat, and insecure execution environments. Yugayu solves this by scaffolding isolated AI entities across a trustless, multi-node network, utilizing cryptographic passports and a centralized immutable ledger.

## Core Architecture

1. **Decoupled Execution:** Global workspaces host deduplicated foundation models, preventing local storage bloat.
2. **Zero-Trust IAM:** AI agents cryptographically sign requests using local `.yugayu-identity` wallets. The `gateway` dynamically blocks execution based on trust scores.
3. **Cryptographic Provenance:** Standard logging is replaced by an immutable ledger, hashing every AI execution against the previous entry.

## Installation & Quickstart

Yugayu uses `uv` for lightning-fast dependency management.

```bash
git clone [https://github.com/yuga-ayu/yugayu-os.git](https://github.com/yuga-ayu/yugayu-os.git)
cd yugayu-os
uv tool install -e .