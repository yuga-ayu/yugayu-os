# Yugayu OS Release Notes
All notable changes to this project will be documented in this file.

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