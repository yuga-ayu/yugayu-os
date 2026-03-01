# Yugayu OS Release Notes
All notable changes to this project will be documented in this file.

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