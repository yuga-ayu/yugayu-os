# Yugayu Protocol: Master Backlog & Roadmap

## 🎯 Active Sprint: Phase 3 (Vision Ayu)
- [ ] Scaffold the first project: `yugayu-vision`.
- [ ] Implement ComfyUI headless API payload generation in the setup hook.
- [ ] Download and link high-fidelity image models (Hunyuan-Image 3.0 / FLUX.2) to the shared workspace.
- [ ] Ensure payload transport routes through the `E2E-Cipher` and `iam-bouncer`.

## 🏦 Tech Debt & Core OS Enhancements
- [ ] **Audit:** Upgrade standard `RotatingFileHandler` to a Cryptographic Merkle Ledger.
- [ ] **Trust:** Implement Honor/Reward Score logic (0.0 to 1.0) and quarantine function for rogue ayus.
- [ ] **Tracking:** Intercept API payloads to calculate token/VRAM usage and write to the ledger.
- [ ] **Compliance:** Build a Cryptographic License Ledger to mandate commercial/non-commercial boundaries for base models.
- [ ] **Storage:** Create a symlink dependency graph to prevent deletion of shared base models.

## ✅ Completed
- [x] **Security:** Implement quantum-resistant asymmetric keypair/encapsulation interfaces (`KeyNegotiator`).

## 🧊 Icebox (Future Architecture)
- [ ] Integrate `vLLM` for local text generation and coding agents.
- [ ] Build a local Web UI dashboard to visualize Lab Status and node health.
- [ ] Ubuntu OS-level PAM integration for human-override access control.