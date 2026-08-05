# ADR-0001: AWS-First Architecture with Local-First Development

## Status

Accepted

## Date

2026-08-05

## Context

RetailPulse is designed as an AWS data engineering platform.

Running every development and smoke-test activity directly in AWS would increase cost,
setup time, credential requirements, and operational complexity during the early phases.

The project also needs a reproducible local environment that can be started, tested,
and cleaned without depending on cloud access.

## Decision

AWS is the target platform for the production architecture.

Local development and Phase 0 smoke testing use Docker Compose, PostgreSQL, Airflow,
Python, and PowerShell.

The local environment is a development and validation baseline. It does not claim to
fully reproduce the future AWS production environment.

Cloud-specific services, infrastructure, security controls, and deployment automation
will be introduced in their assigned later phases.

## Alternatives Considered

- Cloud-only development from the beginning.
- Local-only architecture without an AWS production target.
- Manual local installation without Docker Compose.

## Consequences

### Positive

- Developers can start and test the project without AWS credentials.
- Local setup is faster, cheaper, and reproducible.
- PostgreSQL and Airflow behavior can be validated before cloud deployment.
- The production architecture remains aligned with AWS.

### Negative

- Local services will not reproduce every AWS behavior or limitation.
- Some integration issues will only appear when AWS services are introduced.
- Local and cloud configuration must remain clearly separated.

### Follow-up

- Add AWS infrastructure and managed services only in their planned phases.
- Keep local setup, test, and clean commands working as the project evolves.
- Document differences between local and AWS environments when they become relevant.
