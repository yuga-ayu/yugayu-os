# 🧬 Yugayu OS (Project Parvati)

[![Version: 0.6.0](https://img.shields.io/badge/Version-0.6.0-purple.svg)]()
[![CI Status](https://github.com/yuga-ayu/yugayu-os/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/yuga-ayu/yugayu-os/actions/workflows/ci.yml)
[![License: Dual](https://img.shields.io/badge/License-Fair__Source_(Dual)-blue.svg)](./LICENSE)
![Python](https://img.shields.io/badge/Python-3.11_%7C_3.12-306998.svg?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey.svg?logo=linux)

**Sovereign Intelligence at the Local Network Edge.**

Cloud AI is a black box. You don't own the compute, you don't control the models, and your data is constantly siphoned for telemetry. 

Yugayu OS is a decentralized, local-first operating system designed specifically to govern, isolate, and orchestrate AI entities ("Ayus") directly on your own hardware. It doesn't just run AI scripts; it forces them to operate within a strict framework of cryptographic identity, economic accountability, and telemetry blackouts.

## Core Pillars

1. **Zero-Trust Security:** Every Ayu is issued an Ed25519 cryptographic passport. No execution occurs without identity verification.
2. **Immutable Accountability:** Every execution, success, and failure is hashed to a local, tamper-proof Merkle Ledger. There are no ghost processes.
3. **The Prana Economy:** Compute is finite. The Treasury Wallet enforces a tokenized economy (Prana), escrowing resources before execution to prevent runaway processes.
4. **Hardware Maximization:** Built-in sequential CPU-to-GPU offloading and FP8 staging allows massive models (like FLUX.2-dev) to run flawlessly on consumer GPUs (e.g., RTX 5090).
5. **Absolute Privacy:** Outbound telemetry is aggressively blocked (`HF_HUB_OFFLINE=1`). Your homelab is an air-gapped fortress.

## ⚖️ Fair-Source Dual License

Yugayu OS is strictly Dual-Licensed. **It is NOT an Open-Source project.** * **Free Tier:** 100% free for individual builders, academic researchers, and homelabers for non-commercial use.
* **Commercial Tier:** If you intend to use Yugayu OS for internal business operations, integrate it into a revenue-generating product, or host it as a service (SaaS), a paid commercial license is strictly required. 

See the `LICENSE` file for full terms. For commercial inquiries, contact: **yogi@yugayu.com**

## 🚀 Quickstart

**1. Install the OS (Editable Mode Recommended for Devs)**
```bash
git clone [https://github.com/your-username/yugayu-os.git](https://github.com/your-username/yugayu-os.git)
cd yugayu-os
uv tool install -e .
```bash

**2. Provision the Lab & Mint Your Identity

yugayu setup-lab

**3. Verify System Viability

yugayu verify-lab

**4. Wake an Ayu & Execute
(Requires a valid Ayu manifest, see docs/DEVELOPER_GUIDE.md)

yugayu wakeup-ayu --config-file examples/flux2-config.yaml
yugayu ask image_flux2dev "a futuristic cyberpunk temple