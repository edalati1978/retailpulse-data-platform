# RetailPulse Data Platform

RetailPulse is an end-to-end AWS retail and fulfillment data platform portfolio project.

## Project Goal

The project demonstrates the design and implementation of a data platform for an omnichannel retail business, including store sales, online activity, orders, inventory, fulfillment, and analytics.

## Scope

Version 1.0 focuses on the AWS-based core platform defined in the project master design.

## Data Notice

All generated operational data and benchmark datasets used in this project are synthetic or explicitly identified as benchmark data. This project does not claim production-scale experience.

## Repository Structure

```text
retailpulse-data-platform/
|-- .github/
|   |-- ISSUE_TEMPLATE/
|   `-- workflows/
|-- airflow/
|   `-- dags/
|-- docs/
|   |-- adr/
|   `-- checkpoints/
|-- postgres/
|-- scripts/
|-- tests/
`-- README.md
```

## Prerequisites

The current Phase 0 baseline uses:

- Git
- GitHub
- PowerShell
- Docker Desktop

Additional project tools will be introduced in their relevant phases.

## Quick Start

1. Clone the repository.
2. Enter the repository directory.
3. Confirm that the local branch is synchronized with GitHub.

```powershell
git clone https://github.com/edalati1978/retailpulse-data-platform.git
cd retailpulse-data-platform
git status
```

### Python Environment on PowerShell

From the repository root, allow scripts for the current PowerShell window and activate the virtual environment:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\.venv\Scripts\Activate.ps1
```

A successful activation adds `(.venv)` to the beginning of the PowerShell prompt.

## Commands

```powershell
git status
git log -1 --oneline
git remote -v
```

## Architecture

The detailed platform architecture will be documented as the implementation progresses through its defined phases.

## Current Phase

Phase 0: Baseline and Governance

Current step: Documentation and collaboration rules.

