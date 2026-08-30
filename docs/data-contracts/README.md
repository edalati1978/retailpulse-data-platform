# Data Contract Conventions

## File Naming

- Contract file names use lowercase kebab-case.
- Examples:
  - tpcds.yaml
  - postgres-oltp.yaml
  - events.yaml
  - open-meteo.yaml
- Field names use snake_case.
- File names and field names must be written in English.

## Versioning

Contract and schema versions use:

MAJOR.MINOR.PATCH

- MAJOR: Breaking change that may require consumer changes.
- MINOR: Backward-compatible addition, such as a new optional field.
- PATCH: Documentation correction or clarification without a schema change.

Every contract must include:

- contract_version
- schema_versioning.current_version
- schema_versioning.compatibility_policy
- schema_versioning.breaking_change_policy

## General Rules

- Do not store passwords, tokens, API keys, or private credentials in contracts.
- Clearly label data as synthetic, benchmark, or public.
- Each contract must define the entity grain, keys, schema, quality rules, and limitations.
