# Yugayu OS: Developer & Architecture Guide

Welcome to the internal architecture of Yugayu OS. This document outlines how to provision custom AI entities (Ayus), manage hardware constraints, and understand the core operating system departments.

## 1. System Architecture Overview

Yugayu is not a script wrapper; it is a modular operating system with distinct, zero-trust departments:

* **The Command Router (`core/command_router.py`):** The gateway. It intercepts all CLI commands and verifies the cryptographic signature of the executing actor before routing the payload.
* **The Architect (`core/architect/capability_manager.py`):** The builder. It reads declarative YAML manifests, provisions isolated Python virtual environments, securely downloads/symlinks model weights, and mints the Ayu's identity.
* **The Identity Bouncer & Issuer (`core/security/`):** Manages the Ed25519 cryptographic passports for both the human Admin and the localized Ayus.
* **The Ledger Manager (`core/state/ledger_manager.py`):** The source of truth. Maintains the immutable `config.yaml` state, logging the existence, capabilities, and honor status of every entity.
* **The Treasury (`core/economy/treasury_wallet.py`):** Manages "Prana," the native token of compute. It escrows tokens before execution and refunds/deducts based on success, preventing infinite loops and hardware monopolization.

## 2. Hardware Maximization (The FLUX.2 Breakthrough)

Running state-of-the-art models (like the 30GB+ FLUX.2-dev) on consumer hardware requires strict VRAM orchestration. Yugayu handles this natively via specific PyTorch/Diffusers integrations:

1.  **System RAM Staging:** By explicitly setting `device_map="cpu"` during the initial `from_pretrained` load, Yugayu prevents immediate CUDA Out-Of-Memory (OOM) crashes by parking massive weights in DDR5 RAM.
2.  **FP8 Quantization:** The core transformer is cast to `torch.float8_e4m3fn` in memory, instantly halving its VRAM footprint with zero perceptible quality loss.
3.  **Sub-Model Offloading:** Using `enable_model_cpu_offload()`, Yugayu acts as a traffic controller, shuttling the Text Encoder, Transformer, and VAE in and out of the GPU sequentially over the PCIe bus, keeping peak VRAM comfortably below 32GB.
4.  **Memory De-fragmentation:** The OS injects `PYTORCH_ALLOC_CONF="expandable_segments:True"` into the execution environment to prevent memory fragmentation during heavy generation cycles.

## 3. Provisioning an Ayu (The Manifest)

Ayus are created using a declarative YAML configuration. 

**Example: `flux2-config.yaml`**
```yaml
entity:
  name: "image_flux2dev"
  type: "ayu"
  license_accepted: "bsl-non-commercial"

setup:
  - "uv venv private_data/.venv"
  - "uv pip install --python private_data/.venv torch diffusers transformers accelerate"

resources:
  - name: "flux2-official"
    type: "model_weights"
    shareable: true
    fetch_command: "hf download black-forest-labs/FLUX.2-dev --local-dir {shared_dir}/flux2-official"
  - name: "inference-script"
    type: "code"
    shareable: false
    fetch_command: "cp {repo_dir}/docs/private/image_flux2dev_inference.py {private_dir}/private_data/run_inference.py" 

execution:
  inference_command: >
    private_data/.venv/bin/python private_data/run_inference.py 
    --prompt '{prompt}' 
    --output '{output}' 
    --base_model 'models/flux2-official' {input}
```

To wake the Ayu, run: `yugayu wakeup-ayu --config-file path/to/config.yaml`.

## 4. Physical Isolation Strategy

Yugayu strictly enforces physical file isolation to prevent cross-contamination:
* **`~/yugayu-lab/shared/models/`**: Houses foundational, immutable weights (e.g., base FLUX.2).
* **`~/yugayu-lab/ayus/{name}/`**: The isolated jail for the entity. It contains its private `.venv`, local cryptographic wallet, and symlinks to authorized shared models.