# RetailPulse Data Platform

RetailPulse is an end-to-end AWS retail and fulfillment data engineering portfolio project.

## Project Goal

The project demonstrates the design and implementation of a data platform for an
omnichannel retail business, including sales, online activity, orders, inventory,
fulfillment, and analytics.

All operational data used by the project is synthetic or explicitly identified as
benchmark or public data.

## Architecture Approach

AWS is the target platform for the production architecture.

Docker Compose, PostgreSQL, Airflow, Python, and PowerShell provide the reproducible
local development and validation baseline.

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
|   |-- checkpoints/
|   `-- data-contracts/
|-- postgres/
|-- scripts/
|-- streaming/
|-- tests/
|-- tpcds/
|-- weather/
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

Run the standard local project checks:

```powershell
.\scripts\test.ps1
```

The project also includes Pytest validation for source contracts, sample data,
event schemas, deterministic seed generation, Open-Meteo behavior, and PostgreSQL
integration.

To run the complete Pytest suite including PostgreSQL integration:

```powershell
$env:RUN_POSTGRES_INTEGRATION="1"
python -m pytest
Remove-Item Env:RUN_POSTGRES_INTEGRATION
```

The current Phase 1 validation suite contains:

```text
26 passing tests
```

when PostgreSQL integration is enabled.

## Phase 1 Data Sources

Phase 1 defines and validates four active source families:

- TPC-DS synthetic benchmark data
- PostgreSQL synthetic OLTP data
- Python-generated retail events
- Open-Meteo historical weather data

NOAA GSOD was evaluated as an alternative weather source but is not implemented
in the active project scope.

Data contracts are stored under:

```text
docs/data-contracts/
```

The active contracts are:

```text
events.yaml
open-meteo.yaml
postgres-oltp.yaml
tpcds.yaml
```

## Phase 1 Demo

Run the repeatable Phase 1 validation demo:

```powershell
.\scripts\phase1_demo.ps1
```

The demo validates:

- the four active data contracts
- TPC-DS sample structure
- event schema validation and controlled failure cases
- Open-Meteo client behavior using fixtures and mocks
- PostgreSQL schema and seed integration

A successful run ends with:

```text
=== Phase 1 demo completed successfully ===
```

## PostgreSQL OLTP Source

Phase 1 includes a synthetic PostgreSQL operational source with:

- customers
- inventory
- orders
- order_items

The baseline deterministic dataset contains:

```text
customers:   100
inventory:    50
orders:      500
order_items: 1483
```

The integration test creates an isolated temporary PostgreSQL database, loads the
schema and deterministic seed data, validates expected row counts and order totals,
and removes the temporary database after the test.

## Events

Phase 1 defines a versioned retail event contract and JSON Schema.

Validation includes:

- acceptance of a known-good event
- rejection of an event without `event_id`
- rejection of an unsupported `schema_version`

A production real-time event producer and Kinesis implementation are intentionally
out of scope for Phase 1.

## Open-Meteo

Open-Meteo provides historical daily weather enrichment.

The client supports:

- historical daily weather requests
- configurable timeout
- retry for transient failures
- retry for HTTP 429 and selected HTTP 5xx responses
- deterministic local caching
- fixture-based and mocked tests without CI internet dependency

## Airflow

Open the local Airflow interface:

```text
http://localhost:8080
```

The Phase 0 smoke DAG is named:

```text
retailpulse_smoke
```

Airflow authentication credentials are generated locally and are not committed to Git.

Production ingestion DAGs are not implemented in Phase 1.

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

GitHub Actions runs on pushes and pull requests targeting `main`.

The CI workflow:

- sets up Python 3.12
- installs pinned project and test dependencies
- creates the local environment file from `.env.example`
- starts PostgreSQL with Docker Compose
- runs the full Pytest suite including PostgreSQL integration validation
- runs Ruff
- validates the Docker Compose configuration

The Phase 1 Package 7 CI run completed successfully with all checks green.

## Current Phase

Phase 0: Baseline and Governance

Status: complete.

Phase 1: Source Contracts, Validation, and Demo

Status: complete.

Completed Phase 1 packages:

- Package 0
- Package 1
- Package 2
- Package 3
- Package 4
- Package 5
- Package 6
- Package 7
- Package 8

Phase 2: Raw Ingestion

Status: not started.