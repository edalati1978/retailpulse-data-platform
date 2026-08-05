CREATE TABLE IF NOT EXISTS smoke_check (
    id INTEGER PRIMARY KEY,
    message TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO smoke_check (id, message)
VALUES (1, 'PostgreSQL smoke test passed')
ON CONFLICT (id) DO NOTHING;
