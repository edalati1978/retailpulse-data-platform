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
