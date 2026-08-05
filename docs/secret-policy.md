# Secret Management Policy

1. Real secrets, passwords, tokens, and credentials must never be committed to Git.
2. Only `.env.example` may be committed as the public environment-variable template.
3. If a secret is exposed, it must be changed or rotated immediately.
4. AWS Secrets Manager will be used for secret storage in future AWS environments.
