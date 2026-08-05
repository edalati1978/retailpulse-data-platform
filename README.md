# RetailPulse Data Platform

RetailPulse is an end-to-end AWS retail and fulfillment data engineering portfolio project.

## Project Goal

The project demonstrates the design and implementation of a data platform for an
omnichannel retail business, including sales, online activity, orders, inventory,
fulfillment, and analytics.

All operational data used by the project is synthetic or explicitly identified as
benchmark data.

## Architecture Approach

AWS is the target platform for the production architecture.

Docker Compose, PostgreSQL, Airflow, Python, and PowerShell provide the reproducible
local development and smoke-test baseline.

See:

- [ADR-0001: AWS-First Architecture with Local-First Development](docs/adr/ADR-0001-aws-first-local-first.md)
- [Secret Management Policy](docs/secret-policy.md)

## Repository Structure

```text
retailpulse-data-platform/
|-- .github/
|   |-- ISSUE_TEMPLATE/
|   `-- workflows/
|-- airflow/
|   `-- dags/
|-- docker/
|   `-- postgres/
|       `-- init/
|-- docs/
|   |-- adr/
|   `-- checkpoints/
|-- scripts/
|-- tests/
|-- .env.example
|-- docker-compose.yml
|-- pyproject.toml
`-- README.md
```

## Prerequisites

Install the following tools before running the project:

- Git
- Python 3.12
- PowerShell
- Docker Desktop

Docker Desktop must be running.

## Quick Start

Clone the repository and enter its directory:

```powershell
git clone https://github.com/edalati1978/retailpulse-data-platform.git
cd retailpulse-data-platform
```

Allow local scripts for the current PowerShell window:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
```

Create the Python environment, install development dependencies, create the local
environment file, and start PostgreSQL and Airflow:

```powershell
.\scripts\setup.ps1
```

The setup command waits until both Docker services are healthy.

## Run Tests

Run the complete local smoke-test suite:

```powershell
.\scripts\test.ps1
```

The test command checks:

- Python 3.12
- Pytest
- Ruff
- Docker Compose configuration
- PostgreSQL smoke data
- Airflow smoke DAG

A successful run ends with:

```text
All RetailPulse tests passed.
```

## Airflow

Open the local Airflow interface:

```text
http://localhost:8080
```

The smoke DAG is named:

```text
retailpulse_smoke
```

Airflow authentication credentials are generated locally and are not committed to Git.

## Clean Local Services

Stop and remove local containers and temporary caches:

```powershell
.\scripts\clean.ps1
```

This command preserves Docker volumes, PostgreSQL data, Airflow data, the local `.env`
file, and the Python virtual environment.

Start the environment again with:

```powershell
.\scripts\setup.ps1
```

## Environment and Secrets

Copy `.env.example` to `.env` only for local use.

The setup script performs this copy automatically when `.env` does not exist.

Never commit:

- `.env`
- passwords
- access keys
- tokens
- private credentials

## Continuous Integration

GitHub Actions runs the following checks on pushes and pull requests targeting `main`:

- Pytest
- Ruff
- Docker Compose configuration validation

## Current Phase

Phase 0: Baseline and Governance

Status: final validation and closure.
