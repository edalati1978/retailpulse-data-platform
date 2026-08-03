# Contributing to RetailPulse

This document defines the basic collaboration rules for the project.

## Branch Naming

Use a short, descriptive branch name.

Recommended formats:

- `docs/short-description`
- `feature/short-description`
- `fix/short-description`
- `chore/short-description`

## Commit Messages

Use this format:

```text
type: short description
```

Common types:

- `docs` for documentation
- `chore` for repository or maintenance work
- `feature` for new functionality
- `fix` for corrections
- `test` for test-related changes

Keep each commit focused on one clear change.

## Pull Request Checklist

Before requesting a review:

- Confirm that the change has a clear purpose.
- Run the relevant tests or checks.
- Update documentation when necessary.
- Confirm that no unrelated files are included.
- Confirm that no secrets, credentials, generated data, or large files are committed.
- Confirm that the working tree is clean after the final commit.

## Secrets

Never commit passwords, access keys, API tokens, credentials, or private connection details.

Use placeholders in documentation and local configuration files for sensitive values.
