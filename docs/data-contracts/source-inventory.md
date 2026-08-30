# Phase 1 Source Inventory

Active Phase 1 sources: 4

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
- Update behavior: Inserts occur across the OLTP tables; updates are modeled for customers, orders, and inventory and are tracked with updated_at. order_items currently has created_at only.
- Limitations: Locally generated synthetic operational data; CDC is not implemented in Phase 1

## Python Event Source

- Source type: Event stream definition
- Purpose: Define click, cart, checkout, payment, and order-status events
- Entity and grain: One JSON document represents one event
- Keys: event_id, event_type, schema_version, and event_time
- Update behavior: Append-only events; duplicate and late-event behavior is documented only
- Limitations: Kinesis and controlled event generation are outside Phase 1

## Open-Meteo REST API

- Source type: REST API
- Purpose: Provide historical daily weather enrichment for RetailPulse
- Entity and grain: One logical record represents one geographic location and one calendar date
- Business key: latitude, longitude, and date
- Update behavior: Historical data is requested on demand with timeout, retry, and local cache behavior
- Replay behavior: Repeated requests for the same location and date range may be replayed safely and should not create duplicate downstream weather records
- Limitations: External public API; only selected daily weather variables are included; cloud ingestion and warehouse loading are outside Phase 1

## Evaluated Alternative

### NOAA GSOD on AWS

NOAA GSOD was evaluated as a possible historical weather source during Phase 1 but was not implemented. Open-Meteo is the selected and implemented weather source for the current RetailPulse design.
