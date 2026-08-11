# Phase 1 Source Inventory

## TPC-DS Toolkit

- Source type: Batch benchmark data
- Purpose: Historical retail sales, customer, inventory, store, web, and catalog analysis
- Entity and grain: Defined separately for each selected TPC-DS table
- Keys: Toolkit-defined primary and business keys
- Update behavior: Regenerated batch dataset; not an operational update stream
- Limitations: Synthetic benchmark data and not production retail data

## PostgreSQL OLTP

- Source type: Relational operational source
- Purpose: Simulate customer, order, order-item, and inventory changes
- Entity and grain: One row per customer, order, order item, or inventory record
- Keys: Relational primary keys, foreign keys, and business keys
- Update behavior: Inserts and updates with created_at and updated_at timestamps
- Limitations: Locally generated synthetic operational data; CDC is not implemented in Phase 1

## Python Event Source

- Source type: Event stream definition
- Purpose: Define click, cart, checkout, payment, and order-status events
- Entity and grain: One JSON document represents one event
- Keys: event_id, event_type, schema_version, and event_time
- Update behavior: Append-only events; duplicate and late-event behavior is documented only
- Limitations: Kinesis and controlled event generation are outside Phase 1

## NOAA GSOD on AWS

- Source type: Public S3 dataset
- Purpose: Historical weather enrichment
- Entity and grain: One weather observation for a station and observation date
- Keys: Station identifier and observation date
- Update behavior: Published historical files and periodic additions
- Limitations: Public-source structure must be analyzed; cloud ingestion is outside Phase 1

## Open-Meteo REST API

- Source type: REST API
- Purpose: Weather enrichment and API-client practice
- Entity and grain: One response contains weather values for a location and requested time range
- Keys: Location coordinates, date or timestamp, and requested variables
- Update behavior: Request-based responses with retry, timeout, and cache behavior
- Limitations: API availability, rate behavior, and response changes must be handled
