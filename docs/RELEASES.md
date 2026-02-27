# Yugayu OS Release Notes
All notable changes to this project will be documented in this file.

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

**Core Features Included:**
* **Dynamic CLI Router:** Modular architecture via `main.py` and `registry.py` for hot-swappable commands.
* **Lab Scaffolding:** `setup-lab` command provisions global shared directories and configuration state.
* **Ayu Management:** `create-ayu` initializes isolated Git/UV project environments with auto-generated test suites.
* **Security & IAM:** `gateway.py` implemented for pre-flight authentication and log-size validation.
* **Audit Ledger:** Time-series chunked activity logger configured (20MB soft limit).
* **Automated Testing:** 100% sandboxed Pytest framework with automated JUnit XML tracking configured via Git pre-commit hooks.