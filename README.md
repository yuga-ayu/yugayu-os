# 🧬 Yugayu AI Protocol (Project Parvati - Creator of AI ayu's)

**The Orchestration Protocol for Local AI Systems.**

[![Version: 0.6.0](https://img.shields.io/badge/Version-0.6.0-purple.svg)]()
[![CI Status](https://github.com/yuga-ayu/yugayu-os/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/yuga-ayu/yugayu-os/actions/workflows/ci.yml)
[![License: Dual](https://img.shields.io/badge/License-Fair__Source_(Dual)-blue.svg)](./LICENSE)
![Python](https://img.shields.io/badge/Python-3.11_%7C_3.12-306998.svg?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey.svg?logo=linux)

*Yugayu* translates from Sanskrit as "Life of a New Era" (*Yuga* + *Ayu*). In this ecosystem, an **Ayu** is a distinct, localized AI entity.

Yugayu OS is a foundational AI Operating System and orchestrator for local AI lab projects. It acts as a strict, secure protocol allowing disparate AI models, agents, and tools to be managed under a unified architecture. 

Ultimately, Yugayu is designed to be the bridging protocol that allows a master local LLM to securely coordinate multiple autonomous Ayus—building, executing, and iterating on complex projects as a singular, cohesive system governed by strict cryptographic rules.

## Core Pillars of the Protocol

1. **Zero-Trust Identity:** Every Ayu is issued an Ed25519 cryptographic passport. No execution or inter-system communication occurs without identity verification.
2. **Immutable Accountability:** Every action is hashed to a local, tamper-proof Merkle Ledger. There are no ghost processes; the master orchestrator always has a perfect state history.
3. **The Prana Economy:** Compute is a finite resource. The Treasury Wallet enforces a tokenized economy (Prana), escrowing resources before execution to prevent runaway autonomous loops.
4. **Hardware Maximization:** Built-in sequential CPU-to-GPU offloading and FP8 staging allows massive models (like FLUX.2-dev) to run flawlessly on consumer hardware.
5. **Absolute Privacy:** Outbound telemetry is aggressively blocked (`HF_HUB_OFFLINE=1`). The lab environment remains a physically isolated, air-gapped fortress.

## ⚖️ Fair-Source Dual License

Yugayu OS is strictly Dual-Licensed. **It is NOT an Open-Source project.** * **Free Tier:** 100% free for individual builders, academic researchers, and homelabers for non-commercial use.
* **Commercial Tier:** If you intend to use Yugayu OS for internal business operations, integrate it into a revenue-generating product, or host it as a service (SaaS), a paid commercial license is strictly required. 

See the `LICENSE` file for full terms. For commercial inquiries, contact: **yogi@yugayu.com**

## 🚀 Quickstart

**1. Install the OS (Editable Mode Recommended for Devs)**
```bash
git clone [https://github.com/yuga-ayu/yugayu-os.git](https://github.com/yuga-ayu/yugayu-os.git)
cd yugayu-os
uv tool install -e .
```

**2. Provision the Lab & Mint Your Identity**
```bash
yugayu setup-lab
```

**3. Verify System Viability**
```bash
yugayu verify-lab
```

**4. Wake an Ayu & Execute**
*(Requires a valid Ayu manifest, see `docs/DEVELOPER_GUIDE.md`)*
```bash
yugayu wakeup-ayu --config-file examples/flux2-config.yaml
yugayu ask image_flux2dev "a futuristic cyberpunk temple"
```