# Yugayu OS Release Notes
All notable changes to this project will be documented in this file.

# Yugayu OS Release Notes

## [v0.6.0] - The Sovereign Architecture Release (Current)

This milestone release establishes the foundational architecture of Yugayu OS, proving that massive, state-of-the-art models can be fully governed by a localized, cryptographically secure control plane.

### 🚀 Key Features & Capabilities

* **The Architect Department:** Fully functional declarative provisioning. The OS can now read YAML manifests, construct isolated `.venv` environments, securely download weights, and symlink resources without polluting the host system.
* **Hardware Maximization (FLUX.2 Integration):** Successfully demonstrated the capability to run 30GB+ models on consumer GPUs. Implemented FP8 staging, `device_map="cpu"` initialization, and sequential sub-model offloading to completely bypass CUDA Out-Of-Memory bottlenecks.
* **Telemetry Blackout:** Hardcoded execution gateways that forcefully inject `HF_HUB_OFFLINE=1` and `DISABLE_TELEMETRY=1` into all Ayu environments.
* **Cryptographic Identity (MVP):** Integrated `cryptography` library to mint Ed25519 asymmetric keypairs. Both the Admin CLI and individual Ayus are now issued localized cryptographic passports.
* **Merkle Ledger (MVP):** The `config.yaml` state manager is active, tracking lab roots, installed entities, capabilities, and quarantine statuses.
* **The Prana Economy (MVP):** Established the Treasury Wallet. The OS successfully escrows execution tokens prior to inference and refunds them upon successful artifact generation.

### 🛠️ Developer Tools
* `yugayu dev tree`: Inspect isolated lab environments and OS repositories.
* `yugayu dev run-test`: Trigger the Pytest diagnostic suite from anywhere.
* `yugayu dev export-state`: Advanced AST-parsing state exporter for generating contextual snapshots of the OS.

### 🛣️ Roadmap to v1.0.0
* Upgrade Ed25519 identity keys to Post-Quantum ML-DSA (Dilithium).
* Implement the Dharma Honor System (dynamic compute privileges based on execution success rates).
* Introduce the `engage` persistent session loop to eliminate cold-boot latency.
* Full P2P Encrypted payload routing via Kyber Key Exchange.

## [v0.5.0] - The Agnostic Orchestrator
**Date:** 2026-03-02

**Description:** The pivotal release transitioning Yugayu OS into a fully agnostic, Zero-Trust execution environment. The OS has been stripped of all hardcoded model references (e.g., HuggingFace, Diffusers) and now operates strictly as a hardware resource and identity orchestrator via YAML manifests.

**Core Architecture Implemented:**
* **Agnostic Run Engine:** `run_engine.py` no longer contains AI library logic. It reads `inference_command` payloads from the Ayu's configuration manifest and executes them securely inside isolated `.venv` directories via `subprocess`.
* **Dynamic Scaffolding:** `capability_manager.py` now parses terminal commands directly from the configuration file to dynamically execute environment setup (like `uv venv`) and fetch resources before symlinking.
* **Automated Identity Issuance:** Waking up a new Ayu automatically triggers the `identity_issuer` to mint a dedicated Ed25519 cryptographic passport.
* **State-Driven Diagnostics:** `run-test` now dynamically reads the `os_source_path` from the Ledger, allowing global execution of the isolated Pytest suite from anywhere on the host machine.

## [v0.4.0] - Zero-Trust RBAC & Secure Artifacts
**Date:** 2026-03-01

**Description:** Solidified the Yugayu Cryptographic Gateway and secured the developer footprint. The OS now mathematically enforces execution boundaries distinguishing between human maintainers, administrators, and guest users, while strictly separating public architectural documentation from internal AI operational state.

**Core Architecture Implemented:**
* **Identity Issuer Department:** Centralized Ed25519 cryptographic passport generation (`identity_issuer.py`).
* **Role-Based Access Control (RBAC):** Cryptographic identities now possess immutable roles (`maintainer`, `admin`, `guest`, `ayu`). Guests are mathematically blocked from execution pathways.
* **The Enforcer Protocol:** Failed cryptographic signatures or role bypass attempts now trigger the `enforcer.py` module, quarantining rogue entities on the immutable ledger.
* **State Isolation:** `dev_export_state.py` now automatically routes sensitive system state snapshots and AI instruction sets into a secured, `.gitignore`-protected `docs/private/` directory.
* **Public Documentation:** Released formal `PRODUCT_OVERVIEW.md` and `DEVELOPER_GUIDE.md` outlining the Yugayu Symlink Economy and Cryptographic Gateway.
## [v0.3.0] - Strict Zero-Trust Control Plane
**Date:** 2026-02-28

**Description:** Solidified the core security architecture by eliminating all middleware bypasses and enforcing absolute Zero-Trust verification for every command execution. Established the separation of the Control Plane from the physical hardware realm.

**Core Features Included:**
* **Control Plane Isolation:** Decoupled the OS management layer (`~/.yugayu/`) from the massive physical AI execution lab (`~/yugayu-lab/`).
* **Admin Master Key:** Added automated provisioning of an Ed25519 Cryptographic Master Key for the human administrator, stored securely in the Control Plane.
* **Strict Router Enforcment:** Removed command bypass lists from `command_router.py`. Every action (except genesis bootstrapping) is now mathematically verified by the `iam-bouncer`.
* **Ayu Lifecycle:** Replaced `create-ayu` with the interactive `wakeup-ayu` genesis sequence, enforcing compliance and telemetry checks before instantiation.
* **DevOps Introspection:** Added `export-state` and `run-test` commands to allow the OS to self-diagnose and generate dense context vectors for AI co-developers.
* **Hardened Test Suite:** Reached 100% integration test coverage using isolated Pytest sandboxes (`tmp_path`) that simulate cryptographic environments without altering the host OS.

## [v0.2.0] - Quantum-Resistant E2E Modular Architecture
**Date:** 2026-02-27

**Description:** A massive architectural pivot transitioning the protocol to a military-grade, zero-trust sovereign network utilizing Post-Quantum Cryptography (PQC).

**Core Features Included:**
* **Hot-Swappable Interfaces:** Implemented Python `typing.Protocol` for plug-and-play cryptographic modules.
* **iam-bouncer:** Replaced legacy gateway with a strict, fail-closed asymmetric identity verification module.
* **state-management:** Merged legacy lab configuration and new ephemeral cryptographic session tracking (`SessionState`) into a unified keystore.
* **E2E Transport:** Added `KeyNegotiator` (CRYSTALS-Kyber) and `E2E-Cipher` (AES-256-GCM) interfaces for secure payload transport.
* **Introspection:** Added `yugayu tree` command for rapid lab and repository visualization.

## [v0.1.0] - Alpha Core OS Foundation
**Date:** 2026-02-21

**Description:** Initial release of the Yugayu AI Lab Orchestrator platform. This MVP establishes the distributed architecture scaffolding, zero-trust gateway structure, and automated testing pipeline.