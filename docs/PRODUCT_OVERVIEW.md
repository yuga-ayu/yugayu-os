# Yugayu OS: Product Overview

Yugayu is a source-available, local-first operating system designed to orchestrate state-of-the-art AI models on consumer hardware.

### Key Features

* **Hardware Maximization via Sub-Model Offloading:** Running behemoth models like FLUX.2 natively requires massive VRAM. Yugayu bypasses this constraint by implementing highly optimized `device_map="cpu"` staging and dynamic GPU offloading. Models are loaded into system DDR5 RAM and shuttled into the GPU component-by-component, allowing 32GB consumer GPUs to process workloads that typically require enterprise hardware.
* **Strict Telemetry Blocking:**
  By default, Yugayu intercepts and nullifies all outbound tracking. The environment variables `HF_HUB_OFFLINE=1` and `DISABLE_TELEMETRY=1` are hardcoded into the execution gateway. Your data never leaves your homelab.
* **Physical Isolation (The Lab):**
  Yugayu separates shared baseline weights (`/shared/models`) from private execution environments (`/ayus/{name}/private_data`). This ensures that one compromised or poorly configured entity cannot corrupt the underlying datasets or base models used by others.
* **Interactive Engagements:**
  Beyond single-shot inference commands, Yugayu supports persistent `engage` sessions, keeping heavy models loaded in memory for rapid, continuous generation cycles without cold-boot latency.