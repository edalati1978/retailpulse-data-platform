# TPC-DS Source

## Purpose

TPC-DS provides synthetic historical retail data for the RetailPulse project.

In Phase 1, TPC-DS is used as a reproducible historical batch source for sales, customer, inventory, and retail-channel data. This phase documents the source before ingestion and transformation pipelines are implemented.

## Source Configuration

- TPC-DS Tools version: 4.0.0
- Scale factor: SF1
- Delivery mode: batch
- Raw file format: pipe-delimited `.dat`
- Official schema source: `tpcds/tools-v4.0.0/DSGen-software-code-4.0.0/tools/tpcds.sql`

## Selected Tables

- customer
- inventory
- store_sales
- store_returns
- web_sales
- web_returns
- catalog_sales
- catalog_returns

## Observed Local Data Volume

The following sizes were measured directly from the generated SF1 files in `tpcds/sample/`.

| File | Size (MB) |
|---|---:|
| catalog_returns.dat | 20.41 |
| catalog_sales.dat | 282.20 |
| customer.dat | 12.60 |
| inventory.dat | 225.47 |
| store_returns.dat | 31.23 |
| store_sales.dat | 370.45 |
| web_returns.dat | 9.36 |
| web_sales.dat | 140.07 |

Total size of the eight selected local files: approximately **1.066 GB**.

## Repository Layout

- Full generated data: `tpcds/sample/`
- Small committable samples: `tpcds/samples/`
- Schema snapshot: `tpcds/schema-snapshot.md`
- Data contract: `docs/data-contracts/tpcds.yaml`
- Data dictionary: `docs/data-contracts/data-dictionary.md`

Full generated `.dat` files remain local and are excluded from Git.

The small sample files are retained in Git for documentation, review, examples, and lightweight tests.

## Generation

The TPC-DS generator was built and executed in an Ubuntu 20.04 Docker environment.

A verified generation command recovered from the local PowerShell history is:

```powershell
docker run --rm `
  -v "${PWD}\tpcds\tools-v4.0.0\DSGen-software-code-4.0.0\tools:/work" `
  -v "${PWD}\tpcds:/data" `
  -w /work `
  ubuntu:20.04 `
  bash -lc "mkdir -p /data/sample && ./dsdgen -TABLE customer -SCALE 1 -DIR /data/sample -FORCE"
```

The same generation pattern was also observed in the PowerShell history for:

- inventory
- store_sales
- web_sales
- catalog_sales

The table name is supplied through the `-TABLE` argument while the toolkit version, scale factor, and output directory remain fixed.

The selected `store_returns.dat`, `web_returns.dat`, and `catalog_returns.dat` files are also present locally, but their exact original command lines were not recovered from the available PowerShell history.

## Reproducibility Expectations

The recorded generation configuration is:

- TPC-DS Tools v4.0.0
- scale factor 1
- output directory `tpcds/sample/`
- selected tables listed above

Phase 1 reproducibility checks should verify that the required selected tables are present and that the expected TPC-DS structure is available when the same source configuration is used.

Reproducibility does not require committing the full generated dataset to Git.

## Phase 1 Scope

This TPC-DS package documents:

- toolkit version
- scale factor
- selected tables
- observed local data volume
- official schema source
- small committable samples
- source data contract
- table grain and keys
- generation and reproducibility expectations

S3 ingestion, Spark transformations, Redshift modeling, Kinesis, and other downstream pipeline work are intentionally deferred to later phases.