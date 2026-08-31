\# Phase 1 Checkpoint



\*\*Date:\*\* 2026-08-06

\*\*Phase:\*\* Phase 1 - Source \& Data Contracts

\*\*Status:\*\* Started



\## Baseline



\- Branch: `main`

\- Baseline commit: `5c411b4`

\- Local branch matched `origin/main`

\- Working tree was clean before Phase 1 changes

\- Latest GitHub Actions run was successful

\- Phase 0 checkpoint and README confirmed Phase 0 complete



\## Started Today



\- Created `docs/data-contracts/`

\- Created `docs/checkpoints/phase-1-checkpoint.md`



\## Current Scope



\- Define the source inventory

\- Create a shared data contract template

\- Document schema, grain, keys, update behavior, quality rules, and limitations for each source



\## Out of Scope



\- S3 ingestion

\- Spark transformations

\- Redshift

\- Kinesis

\- New Airflow DAGs

\- Terraform

\- Dashboards



\## Next Step



Create the Phase 1 source inventory and:



`docs/data-contracts/contract-template.yaml`


## TPC-DS Source Status

Status: Complete

- Official TPC-DS v4.0.0 toolkit used as the schema source.
- Eight selected table sample fixtures are available under `tpcds/samples/`.
- Each sample fixture contains 5 rows for local development and CI.
- Pytest verifies required sample files exist.
- Pytest verifies each sample file contains exactly 5 rows.
- Pytest verifies each sample row has the expected field count from the official `tpcds.sql` DDL.
- TPC-DS tests currently pass: 3 passed.
- Large generated TPC-DS data and toolkit artifacts remain local/ignored rather than committed to Git.
## Package 3 — PostgreSQL OLTP — COMPLETE

PostgreSQL OLTP source implementation is complete.

Completed artifacts:

- `postgres/schema.sql`
- `postgres/seed.py`
- `postgres/generated/`
- `postgres/sample_queries.sql`
- `postgres/update_scenarios.sql`
- `docs/data-contracts/postgres-oltp.yaml`
- PostgreSQL OLTP section added to `docs/data-contracts/data-dictionary.md`

Validated:

- deterministic seed generation with seed `42`
- 100 customers
- 50 inventory products
- 500 orders
- 1483 order items
- PostgreSQL schema creation
- deterministic seed load
- order-total reconciliation
- foreign-key integrity
- sample queries
- customer update scenario
- order-status update scenario
- inventory update scenario

Relevant commits:

- `29cae72` — PostgreSQL OLTP schema and deterministic seed data
- `f52a435` — Ruff fixes for seed generator
- `7f1bf0e` — PostgreSQL OLTP sample queries
- `3c55330` — PostgreSQL OLTP update scenarios
- `497fcc8` — PostgreSQL OLTP data contract
- `bd81a55` — PostgreSQL OLTP data dictionary

Next Phase 1 package:

**Package 4 — Events / JSON Schema**

Do not redo Package 3 work unless a later change requires re-validation.
## Package 4 — Event Schema & Contract — COMPLETE

Event source definition for future streaming is complete.

Completed artifacts:

- `streaming/event.schema.json`
- `streaming/sample_valid_event.json`
- `streaming/sample_invalid_event.json`
- `docs/data-contracts/events.yaml`
- Event section added to `docs/data-contracts/data-dictionary.md`
- `jsonschema==4.26.0` added to development dependencies in `pyproject.toml`

Defined event types:

- `click`
- `cart`
- `checkout`
- `payment_status`
- `order_status`

Common event envelope:

- `event_id`
- `event_type`
- `schema_version`
- `event_time`
- `producer`
- `payload`

Validated:

- valid event accepted by JSON Schema
- event without `event_id` rejected
- unsupported `schema_version` rejected

Phase 1 scope decisions:

- no real-time producer implemented yet
- no Kinesis producer or consumer implemented yet
- duplicate and late-event behavior defined contractually for future streaming work

Relevant commit:

- `3863dd9` — RetailPulse event schema and contract

Next Phase 1 package:

**Package 5 — Weather / Open-Meteo**

Do not redo Package 4 unless a later schema change requires re-validation.

## Package 5 — Weather / Open-Meteo — COMPLETE

Open-Meteo is the only implemented weather source for RetailPulse.

NOAA GSOD was evaluated as an alternative but is not implemented in the current project scope.

Completed artifacts:

- `weather/open_meteo_client.py`
- `weather/README.md`
- `weather/fixtures/open_meteo_sample.json`
- `docs/data-contracts/open-meteo.yaml`
- `tests/test_open_meteo.py`
- `requests==2.34.2` added to project dependencies
- `weather/cache/` excluded from Git

Implemented client behavior:

- daily historical weather requests
- UTC daily aggregation
- configurable request timeout
- retry for timeout and connection failures
- retry for HTTP 429, 500, 502, 503, and 504
- exponential retry delay
- immediate failure for non-retryable HTTP errors
- deterministic local cache by location and date range
- cache hit avoids unnecessary API calls

Selected daily variables:

- `temperature_2m_max`
- `temperature_2m_min`
- `precipitation_sum`
- `weather_code`

Validated:

- request parameters are built correctly
- cache hit returns cached data without calling the API
- retryable HTTP failure triggers retry
- successful API response is returned and written to cache
- non-retryable HTTP error does not retry
- Open-Meteo tests: 5 passed
- full project tests: 9 passed
- Ruff checks pass for Open-Meteo client and tests

Next Phase 1 package:

**Package 6 — Unified contracts, data dictionary, and sample pack**

Do not redo Package 5 unless a later requirement requires re-validation.

## Package 6 - Unified Contracts, Data Dictionary, and Sample Pack - COMPLETE

Active Phase 1 sources: 4

- TPC-DS
- PostgreSQL OLTP
- Python Events
- Open-Meteo

NOAA GSOD remains documented only as an evaluated alternative and is not an active or implemented source.

Package 6 audit completed:

- contract top-level structure and naming are consistent across all four active sources
- metadata requirements were reviewed and reconciled with source-provided versus future pipeline-generated metadata
- grain and key semantics were verified for all active sources
- PostgreSQL update semantics were corrected to reflect `updated_at` only for customers, orders, and inventory
- event duplicate, replay, schema-version, and event-time semantics were verified
- Open-Meteo replay, cache, and business-key semantics were verified
- TPC-DS regeneration and batch semantics were verified
- sample references for all active sources were verified
- Open-Meteo daily weather fields were added to the data dictionary
- stale `noaa-gsod.yaml` example was removed from the data-contract conventions README
- NOAA references were retained only where explicitly documented as an evaluated alternative
- missing Description columns in older dictionary sections were reviewed and are not treated as a Package 6 blocker

Validation evidence:

- `git diff --check` passed
- full project tests: 9 passed

Next Phase 1 package:

**Package 7 - Tests, controlled failure, and demo**

Do not redo Package 6 unless a later requirement requires re-validation.

## Package 7 - Tests, Controlled Failure, and Demo - COMPLETE

Package 7 added executable validation across all four active Phase 1 sources.

Active Phase 1 sources:

- TPC-DS
- PostgreSQL OLTP
- Python Events
- Open-Meteo

New Package 7 artifacts:

- `tests/test_events.py`
- `tests/test_postgres_integration.py`
- `tests/test_postgres_seed.py`
- `tests/test_contracts.py`
- `scripts/phase1_demo.ps1`
- `PyYAML==6.0.2` added to dev dependencies
- GitHub Actions CI updated to start PostgreSQL and run the PostgreSQL integration test

Event validation:

- valid event sample is accepted
- missing `event_id` is rejected
- unsupported `schema_version` is rejected
- event tests: 3 passed

PostgreSQL operational state verified during Package 7:

- Docker PostgreSQL service: healthy
- PostgreSQL user: `retailpulse`
- PostgreSQL database: `retailpulse`
- public tables present:
  - `customers`
  - `inventory`
  - `orders`
  - `order_items`
  - `smoke_check`
- loaded baseline row counts:
  - customers: 100
  - inventory: 50
  - orders: 500
  - order_items: 1483

PostgreSQL integration validation:

- integration test creates an isolated temporary database: `retailpulse_phase1_test`
- `postgres/schema.sql` is loaded into the temporary database
- deterministic seed data is loaded
- expected customer, inventory, and order counts are verified
- order-item data is verified as non-empty
- `order_total` is verified against the sum of line-item quantity multiplied by unit price
- temporary integration-test database is removed after the test
- PostgreSQL integration test: 1 passed
- Windows UTF-8/BOM handling was explicitly added to the integration test

Deterministic seed validation:

- `postgres/seed.py` is executed twice with the same seed and inputs
- generated `customers.csv`, `inventory.csv`, `orders.csv`, `order_items.csv`, and `load_seed.sql` are compared byte-for-byte
- deterministic seed test: 1 passed

Data contract validation:

- active contracts tested:
  - `events.yaml`
  - `open-meteo.yaml`
  - `postgres-oltp.yaml`
  - `tpcds.yaml`
- `contract-template.yaml` is intentionally excluded from active-source validation
- required contract sections are validated
- source and entity identity fields are validated
- schema version is validated
- referenced sample paths are validated
- required fields are checked against declared schemas where fields are explicitly listed
- contract tests: 12 passed

GitHub Actions CI behavior:

- PostgreSQL is started with:
  - `docker compose up -d --wait postgres`
- `RUN_POSTGRES_INTEGRATION=1` is set during CI pytest execution
- PostgreSQL integration is therefore executed in GitHub Actions rather than skipped
- ordinary local pytest may skip the PostgreSQL integration test when PostgreSQL integration is not explicitly enabled

Phase 1 demo:

- repeatable demo script: `scripts/phase1_demo.ps1`
- demo lists the four active contracts
- TPC-DS sample validation: 3 passed
- Event validation: 3 passed
- Open-Meteo validation: 5 passed
- PostgreSQL integration: 1 passed
- Data contract validation: 12 passed
- demo completed successfully end-to-end

Final local Package 7 validation:

- full test suite with PostgreSQL integration enabled: 26 passed
- Ruff: all checks passed
- no skipped tests when PostgreSQL integration is enabled

Current full test composition:

- smoke: 1
- TPC-DS: 3
- Open-Meteo: 5
- Events: 3
- PostgreSQL integration: 1
- PostgreSQL deterministic seed: 1
- Data contracts: 12
- total: 26

Next Phase 1 package:

**Package 8 - Final documentation, handoff, Git/CI closure**

Do not redo Package 7 unless a later requirement changes implementation or validation behavior.

## Package 8 - Final Documentation, Handoff, and Phase 1 Closure

Status: COMPLETE upon successful CI for the final Phase 1 closure commit.

Completed closure work:

- README updated to reflect the implemented Phase 1 source set and validation state
- Phase 1 demo path documented: `scripts/phase1_demo.ps1`
- PostgreSQL sample-query path documented: `postgres/sample_queries.sql`
- Phase 1 handoff created: `docs/checkpoints/phase-1-handoff.md`
- Phase 2 handoff aligned with the RetailPulse master design
- Phase 2 identified as Raw Ingestion
- Phase 2 implementation has not started
- active Phase 1 sources remain:
  - TPC-DS
  - PostgreSQL OLTP
  - Python Events
  - Open-Meteo
- NOAA GSOD remains an evaluated alternative and is not an active source
- Package 7 validation evidence remains:
  - 26 tests passed with PostgreSQL integration enabled
  - Ruff passed
  - repeatable Phase 1 demo passed
  - GitHub Actions CI passed

Interview-question practice is intentionally deferred by the user until after technical Phase 1 closure and will be handled as a separate interview-preparation activity rather than as a repository artifact.

Final Phase 1 closure conditions:

- final Phase 1 changes committed
- final commit pushed to `main`
- GitHub Actions CI green
- working tree clean

Once those conditions are verified, Phase 1 is formally complete and Phase 2 may begin.