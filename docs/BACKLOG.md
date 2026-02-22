# Yugayu Protocol: Master Backlog & Roadmap

## 🎯 Active Sprint: Phase 2 (Vision Ayu)
- [ ] Scaffold the first project: `real-image-gen`.
- [ ] Implement ComfyUI headless API payload generation in the setup hook.
- [ ] Download and link FLUX.1 [dev] weights to the shared workspace.

## 🏦 Tech Debt & Core OS Enhancements
- [ ] **Security:** Implement ML-DSA (Dilithium) quantum-resistant asymmetric keypair generation for Ayu wallets.
- [ ] **Audit:** Upgrade standard `RotatingFileHandler` to a Cryptographic Merkle Ledger.
- [ ] **Trust:** Implement Honor/Reward Score logic (0.0 to 1.0) and quarantine function for rogue Ayus.
- [ ] **Tracking:** Intercept ComfyUI/vLLM API payloads to calculate token/VRAM usage and write to the ledger.
- [ ] **Compliance:** Build a Cryptographic License Ledger to mandate commercial/non-commercial boundaries for base models.
- [ ] **Storage:** Create a symlink dependency graph to prevent deletion of shared base models.

## 🧊 Icebox (Future Architecture)
- [ ] Integrate `vLLM` for local text generation and coding agents.
- [ ] Build a local Web UI dashboard to visualize Lab Status and node health.
- [ ] Ubuntu OS-level PAM integration for human-override access control.