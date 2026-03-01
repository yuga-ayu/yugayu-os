# Yugayu OS: AI Master Context & Protocol Definition

**File Purpose:** This document serves as the absolute "memory" and dense context vector for AI assistants working on the Yugayu OS codebase. Read this carefully before suggesting code.

## 1. Core Philosophy & Definition
Yugayu OS (codenamed Project Parvati) is a Distributed, Zero-Trust AI Operating System. 
* **The Problem:** Modern AI models are monolithic, phone home (telemetry), break licenses, and fracture local hardware (VRAM exhaustion).
* **The Solution:** We do not "run applications." We orchestrate isolated AI lifeforms called **Ayus**. The OS provides the physical resources (compute, storage), while the Ayus must cryptographically earn the right to execute via a finite token economy.

## 2. System Architecture & Isolation
The operating system enforces strict separation of concerns:
* **The Control Plane (`~/.yugayu/`):** The absolute source of truth. Contains the OS `config.yaml`, the daily execution audit logs, and the Administrator's Cryptographic Master Key (`admin-identity.json`). Capable of rebuilding a destroyed lab from scratch.
* **The Physical Realm (`~/yugayu-lab/`):** Stores the massive 100GB+ model weights (e.g., FLUX.2), vector databases, shared datasets, and the isolated execution workspaces for the individual Ayus.

## 3. The Blockchain Identity Protocol (The Merkle Ledger)
* **Zero-Trust Middleware:** `command_router.py` mathematically verifies every single payload signature against an entity's `.yugayu-identity` via the `iam-bouncer`. There are no bypasses.
* **Tamper-Proof:** Every execution and dependency link is logged. If a library's hash changes unexpectedly, the Core immediately quarantines the entity.
* **Portability:** Ayus can be transplanted between Yugayu labs by presenting their immutable ledger history.

## 4. Hardware Topology (Irvine Lab)
* **Compute Node:** NVIDIA RTX 5090 (32GB VRAM), AMD Ryzen 9950X3D.
* **Vector/Control Nodes:** Dell mt5325 Workstations (Intel Xeon, 64GB ECC).
* **Storage Backbone:** Proxmox Server (Ryzen 7600).

## 5. Operational State (v0.3.0)
* **Active Components:** CLI router dynamically loads plugins based on environment flags. The system is stabilized with 100% isolated test coverage.
* **Capabilities:** The execution engine utilizes a "Skill Registry". Shared resources are stored in the core lab and symlinked.
* **Active Tasks/Backlog:**
  1. Transition the simulated `run_engine.py` to interface with the actual ComfyUI headless API.
  2. Implement local text generation (vLLM) for coding agents.
  3. Expand the `license_warden.py` to actively parse HuggingFace header data.

## 6. Strict Directives for AI Assistants
* **Telemetry:** You must explicitly disable HuggingFace and tracking telemetry in all python code (`HF_HUB_OFFLINE=1`).
* **Licensing:** Only recommend Open Source models with open weights. 
* **Tone/Naming:** Code structures should mimic professional enterprise software (Security, Economy, State, Execution). The biological/Sanskrit naming (Prana, Karma, Ayu) is reserved strictly for overarching concepts, documentation lore, and user-facing CLI output.