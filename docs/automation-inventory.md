# Automation Inventory

This document records every automated mechanism used by the RetailPulse project.
No automation should be introduced or relied on without being documented here.

## GitHub Actions CI

### Purpose

Automatically verify the repository's basic code quality, Python tests, and
Docker Compose configuration in a clean GitHub-hosted environment.

### Workflow file

`.github/workflows/ci.yml`

### Trigger

The workflow runs automatically when:

- code is pushed to the `main` branch
- a pull request targets the `main` branch

There is currently no `workflow_dispatch` trigger, so the workflow does not
have a manually configured GitHub Actions run trigger.

### Permissions

`contents: read`

The workflow receives read-only access to repository contents.

### Job

Job name: `quality`

Runner: `ubuntu-latest`

Maximum runtime: `10 minutes`

### Automated steps

1. Check out the repository
   - Uses: `actions/checkout@v6`

2. Set up Python 3.12
   - Uses: `actions/setup-python@v6`

3. Install development dependencies
   - Command: `python -m pip install pytest==9.1.1 ruff==0.16.1`

4. Create the temporary CI environment file
   - Command: `Copy-Item .env.example .env`

5. Run Python tests
   - Command: `python -m pytest`

6. Run Ruff
   - Command: `python -m ruff check .`

7. Validate Docker Compose configuration
   - Command: `docker compose config --quiet`

### Results and logs

Results are available in:

`GitHub repository -> Actions -> CI -> workflow run -> quality`

Each step has its own execution log.

### Manual reproduction

The individual validation commands can be run locally from the repository
using the project's development environment.

### How to change or disable it

Edit `.github/workflows/ci.yml`.

Changing its triggers or steps changes the automation behavior.

The workflow can also be disabled from GitHub Actions or removed from the
`.github/workflows/` directory if the project intentionally no longer needs it.

### Important behavior

The GitHub runner is temporary. Files created during the workflow, including
the CI `.env` file, do not modify the developer's local machine and disappear
when the runner is destroyed.

## PostgreSQL Initialization Smoke Script

### Purpose

Verify that a newly initialized PostgreSQL database can successfully execute
the project's initialization SQL.

### Script file

`docker/postgres/init/001_smoke.sql`

### Trigger

The script is executed automatically by the official PostgreSQL container
entrypoint when PostgreSQL initializes a new, empty data directory.

It is not automatically executed again during normal container restarts when
the existing PostgreSQL data volume is reused.

### Automated actions

The script:

1. Creates the `smoke_check` table if it does not already exist.
2. Inserts one smoke-test record with `id = 1`.
3. Ignores the insert if the same primary-key record already exists.

### Results and logs

The primary result is stored in the PostgreSQL table:

`smoke_check`

PostgreSQL container initialization logs can be inspected with:

`docker compose logs postgres`

### Manual reproduction

The script can be executed manually against the running PostgreSQL container:

`docker compose exec postgres sh -lc 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /docker-entrypoint-initdb.d/001_smoke.sql'`

### How to change or disable it

Edit or remove:

`docker/postgres/init/001_smoke.sql`

The initialization directory mount is configured in:

`docker-compose.yml`

Changing or removing the script affects future fresh database initialization.
It does not automatically undo or rerun changes in an already initialized
PostgreSQL data volume.

### Important behavior

This is an initialization smoke test, not a complete PostgreSQL health or
application-level test.


## PostgreSQL Container Healthcheck

### Purpose

Continuously verify that the running PostgreSQL container is ready to accept
database connections.

### Configuration file

`docker-compose.yml`

### Trigger

Docker runs this healthcheck automatically while the PostgreSQL container is
running.

### Automated command

`pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}`

Configuration:

- interval: `5 seconds`
- timeout: `5 seconds`
- retries: `10`

### Results

The container health status can be viewed with:

`docker compose ps`

Detailed health information can also be inspected with Docker container
inspection commands.

### Manual reproduction

When the PostgreSQL service is running:

`docker compose exec postgres sh -lc 'pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"'`

### How to change or disable it

Edit or remove the PostgreSQL `healthcheck` section in:

`docker-compose.yml`

### Important behavior

This healthcheck verifies PostgreSQL readiness. It does not validate
RetailPulse tables, data correctness, or application-level behavior.


## Airflow Container Healthcheck

### Purpose

Continuously verify that the running Airflow service responds successfully to
its health endpoint.

### Configuration file

`docker-compose.yml`

### Trigger

Docker runs this healthcheck automatically while the Airflow container is
running.

### Automated command

`curl --fail http://localhost:8080/api/v2/monitor/health || exit 1`

Configuration:

- interval: `10 seconds`
- timeout: `10 seconds`
- retries: `12`
- start period: `60 seconds`

### Results

The container health status can be viewed with:

`docker compose ps`

Detailed health information can also be inspected with Docker container
inspection commands.

### Manual reproduction

When the Airflow service is running:

`docker compose exec airflow curl --fail http://localhost:8080/api/v2/monitor/health`

### How to change or disable it

Edit or remove the Airflow `healthcheck` section in:

`docker-compose.yml`

### Important behavior

This healthcheck verifies that the Airflow service responds to its health
endpoint. It does not prove that every DAG or pipeline is working correctly.


## Local Setup Script

### Purpose

Prepare the local RetailPulse development environment and start the project's
Docker services with a consistent setup process.

### Script file

`scripts/setup.ps1`

### Trigger

Manual only.

The script runs only when a developer explicitly executes it.

### Automated actions

The script:

1. Verifies that Python 3.12 is available.
2. Creates `.venv` if it does not already exist.
3. Upgrades `pip`.
4. Installs:
   - `pytest==9.1.1`
   - `ruff==0.16.1`
   - `PyYAML==6.0.3`
5. Creates `.env` from `.env.example` if `.env` does not exist.
6. Runs:

   `docker compose up -d`

7. Waits up to 120 seconds for:
   - `postgres`
   - `airflow`

   to report a healthy container status.

8. Prints the final Docker Compose status.

### Results and logs

Setup progress and failures are printed in the PowerShell terminal.

Docker service status can be checked with:

`docker compose ps`

Container logs can be inspected with:

`docker compose logs`

### Manual execution

From the repository root:

`.\scripts\setup.ps1`

### How to change or disable it

Edit or remove:

`scripts/setup.ps1`

### Important behavior

The script does not recreate `.venv` or `.env` when they already exist.

It starts the Docker Compose services but does not delete existing Docker
volumes or PostgreSQL data.


## Local Test Script

### Purpose

Run the project's main local validation checks in one repeatable command.

### Script file

`scripts/test.ps1`

### Trigger

Manual only.

The script runs only when a developer explicitly executes it.

### Automated actions

The script:

1. Verifies that `.venv` exists.
2. Runs Python tests with:

   `python -m pytest`

3. Runs Ruff with:

   `python -m ruff check .`

4. Validates Docker Compose configuration with:

   `docker compose config --quiet`

5. Verifies the PostgreSQL smoke-test record in the `smoke_check` table.
6. Tests the Airflow DAG:

   `retailpulse_smoke`

7. Stops immediately if any required validation step fails.

### Results and logs

Results are printed directly in the PowerShell terminal.

Successful completion prints:

`All RetailPulse tests passed.`

### Manual execution

From the repository root:

`.\scripts\test.ps1`

### How to change or disable it

Edit or remove:

`scripts/test.ps1`

### Important behavior

The PostgreSQL and Airflow checks require their Docker services to already be
running.

This script performs validation only. It does not start the services.


## Local Clean Script

### Purpose

Stop local RetailPulse Docker services and remove development cache files.

### Script file

`scripts/clean.ps1`

### Trigger

Manual only.

The script runs only when a developer explicitly executes it.

### Automated actions

The script:

1. Runs:

   `docker compose down`

2. Removes:
   - `.pytest_cache`
   - `.ruff_cache`

3. Removes project `__pycache__` directories outside `.venv`.

### Results and logs

The script prints its result in the PowerShell terminal.

Successful completion prints:

`RetailPulse local services stopped and caches removed.`

### Manual execution

From the repository root:

`.\scripts\clean.ps1`

### How to change or disable it

Edit or remove:

`scripts/clean.ps1`

### Important behavior

The script does not use `docker compose down -v`.

Therefore, Docker named volumes such as PostgreSQL data are preserved.

It also does not remove:

- `.venv`
- `.env`
- source code
- committed project files


## Airflow Smoke DAG

### Purpose

Verify that Airflow can successfully load and execute a minimal RetailPulse DAG.

### DAG file

`airflow/dags/retailpulse_smoke.py`

### Trigger

The DAG has:

`schedule=None`

Therefore, it is not executed automatically on a schedule.

Airflow can load and display the DAG while the Airflow service is running, but
an actual DAG run requires an explicit manual or external trigger.

### Automated actions

The DAG contains one task:

`run_smoke_test`

The task executes a Python function that prints:

`RetailPulse Airflow smoke test passed`

### Results and logs

When executed through Airflow, task results and logs are available through the
Airflow interface.

Container-level logs can also be inspected with:

`docker compose logs airflow`

### Manual execution

The project test script executes the DAG with:

`docker compose exec -T airflow airflow dags test retailpulse_smoke`

### How to change or disable it

Edit or remove:

`airflow/dags/retailpulse_smoke.py`

Changing the DAG's `schedule` changes whether Airflow may create scheduled runs.

### Important behavior

The DAG currently uses `schedule=None`, so it is not a scheduled automation.

Its `start_date` does not by itself create scheduled runs.

This DAG is only a smoke test and does not perform RetailPulse data ingestion,
transformation, or orchestration.

