# Contributing to Yugayu OS (Project Parvati)

First, thank you for considering contributing to the Yugayu AI Orchestration Protocol. It is people like you that make open-source infrastructure robust and scalable.

As a foundational Zero-Trust AI Operating System, we maintain high standards for code quality, security, and architectural consistency. This document outlines the process for contributing to the project.

## Code of Conduct
By participating in this project, you agree to abide by our [Code of Conduct](./CODE_OF_CONDUCT.md). We expect all contributors to maintain a professional and collaborative environment.

## How to Contribute

### 1. Reporting Bugs
If you find a bug in the protocol, state management, or IAM gateway, please open an issue. Provide as much context as possible:
* A clear, descriptive title.
* Steps to reproduce the behavior.
* Expected vs. actual behavior.
* Your environment details (OS, Python version, `uv` version, VRAM specs if applicable).

### 2. Suggesting Enhancements
We welcome architectural discussions and feature requests. When proposing a new feature:
* Explain **why** this enhancement is necessary (e.g., how it improves execution decoupling or cryptographic provenance).
* Provide a conceptual overview of how it should be implemented.
* If it modifies the core orchestration protocol, please draft an Architecture Decision Record (ADR) in the issue description.

### 3. Pull Requests
We use a standard fork-and-pull workflow. 
1. **Fork** the repository and create your branch from `main`.
2. **Commit** your changes with clear, descriptive commit messages.
3. **Test** your changes thoroughly. Ensure that no existing isolation boundaries or IAM constraints are bypassed by your code.
4. **Document** any new CLI commands, API endpoints, or architectural shifts in the `docs/` directory.
5. **Open a PR** and link it to the relevant issue.

### Local Development Setup
1. Clone your fork: `git clone https://github.com/YOUR_USERNAME/yugayu-os.git`
2. Install dependencies using `uv`: `uv tool install -e .`
3. Run the test suite before submitting a PR (refer to the CI workflow for the current testing commands).

Thank you for helping build the future of decoupled AI execution.