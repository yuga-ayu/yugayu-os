# Yugayu OS - Command Line Interface Reference

This document outlines the available CLI commands for interacting with the Yugayu Orchestration Protocol.

## Global Commands

### `yugayu setup_lab`
Initializes the global Yugayu Hub environment.
* **Action:** Creates the `~/yugayu-lab` directory structure and the global `state-management` configuration file.
* **Usage:** `yugayu setup_lab`

### `yugayu status`
Reports the health and status of the Hub.
* **Action:** Verifies the existence of the `state-management` configuration and lists active isolated ayus.
* **Usage:** `yugayu status`

### `yugayu tree <target>`
Introspection tool for visualizing directory structures.
* **Arguments:** * `repo`: Prints the tree of the current source code repository.
  * `lab`: Prints the tree of the initialized `~/yugayu-lab`.
* **Usage:** `yugayu tree lab`

## Entity (Ayu) Management

### `yugayu create-ayu <name>`
Scaffolds a new, isolated AI entity (ayu) within the Zero-Trust environment.
* **Action:** * Creates an isolated directory in `~/yugayu-lab/ayus/<name>`.
  * Initializes Git and a `uv` Python environment.
  * Generates a cryptographic `.yugayu-identity` wallet for the `iam-bouncer`.
* **Usage:** `yugayu create-ayu my-vision-agent`

### `yugayu activity`
Reads the immutable audit ledger.
* **Action:** Outputs the execution history, tracking intercepted commands and validation statuses from the `iam-bouncer`.
* **Usage:** `yugayu activity`