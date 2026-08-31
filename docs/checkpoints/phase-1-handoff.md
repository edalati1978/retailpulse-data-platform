# Phase 1 Handoff

## Status

Phase 1 is complete from a source-definition, contract, sample-data, validation, and demo perspective.

Phase 2 ingestion implementation has not started.

## Active Phase 1 Sources

### TPC-DS

Purpose:
Synthetic benchmark retail history.

Contract:
`docs/data-contracts/tpcds.yaml`

Sample data:
`tpcds/samples/`

Selected tables:

- customer
- inventory
- catalog_returns
- store_returns
- web_returns
- web_sales
- catalog_sales
- store_sales

Important limitation:

- Scale factor 1
- selected tables only
- generated benchmark files remain local where excluded from Git

### PostgreSQL OLTP

Purpose:
Synthetic operational retail source.

Contract:
`docs/data-contracts/postgres-oltp.yaml`

Schema:
`postgres/schema.sql`

Seed generator:
`postgres/seed.py`

Generated baseline:
`postgres/generated/`

Tables:

- customers
- inventory
- orders
- order_items

Baseline row counts verified during Phase 1:

- customers: 100
- inventory: 50
- orders: 500
- order_items: 1483

Important limitations:

- synthetic data only
- single-currency model using USD
- inventory represents one current global state per SKU
- real CDC is not implemented

### Python Events

Purpose:
Synthetic behavioral and order-related event source for future streaming ingestion.

Contract:
`docs/data-contracts/events.yaml`

JSON Schema:
`streaming/event.schema.json`

Valid sample:
`streaming/sample_valid_event.json`

Controlled invalid sample:
`streaming/sample_invalid_event.json`

Validated failure behavior:

- missing `event_id` is rejected
- unsupported `schema_version` is rejected

Important limitations:

- no production event producer
- no Kinesis producer or consumer
- duplicate and late-event behavior are defined contractually but not implemented as a streaming system

### Open-Meteo

Purpose:
Historical daily weather enrichment.

Contract:
`docs/data-contracts/open-meteo.yaml`

Client:
`weather/open_meteo_client.py`

Fixture:
`weather/fixtures/open_meteo_sample.json`

Validated behavior:

- request parameter construction
- local cache
- retryable HTTP failures
- successful response caching
- non-retryable HTTP failures

Important limitations:

- external API availability is outside RetailPulse control
- selected daily variables only
- cloud ingestion and warehouse loading are not implemented

## Data Contracts

Active contracts:

- `docs/data-contracts/events.yaml`
- `docs/data-contracts/open-meteo.yaml`
- `docs/data-contracts/postgres-oltp.yaml`
- `docs/data-contracts/tpcds.yaml`

Template:

- `docs/data-contracts/contract-template.yaml`

The template is not an active source contract.

## Sample Queries

PostgreSQL sample queries:

`postgres/sample_queries.sql`

The query file demonstrates:

- source-table row counts
- customer and order joins
- verification of order totals against line items
- low-inventory inspection
## Validation

Phase 1 currently contains 26 passing tests when PostgreSQL integration is enabled.

Validation includes:

- Python environment smoke test
- TPC-DS sample validation
- Open-Meteo client tests
- event schema tests
- PostgreSQL integration test
- deterministic PostgreSQL seed test
- data-contract tests

Ruff checks pass.

GitHub Actions runs the full test suite including PostgreSQL integration.

## Demo

Repeatable Phase 1 demo:

`.\scripts\phase1_demo.ps1`

The demo validates:

- active data contracts
- TPC-DS samples
- events
- Open-Meteo
- PostgreSQL integration

Expected successful completion:

`=== Phase 1 demo completed successfully ===`

## Phase 2 Starting Point

Phase 2 is defined by the RetailPulse master design as:

**Phase 2 - Raw Ingestion**

Planned Phase 2 work:

- batch upload
- API ingestion
- manifests
- ingestion metadata
- raw data layout

Primary Phase 2 tools:

- Python
- Amazon S3
- AWS IAM

Expected Phase 2 outputs:

- immutable raw partitions
- ingestion audit table

Key engineering topics:

- ingestion
- retry behavior
- checksums
- security

Phase 2 should use the Phase 1 source contracts, schemas, samples, and documented source behavior as its input baseline rather than redefining those sources.

The four active sources entering Phase 2 are:

- TPC-DS
- PostgreSQL OLTP
- Python Events
- Open-Meteo

NOAA GSOD remains an evaluated alternative and is not an active source.

Phase 2 implementation has not started.