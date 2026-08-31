import os
import subprocess
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PROJECT_ROOT / "postgres" / "schema.sql"
LOAD_SEED_PATH = PROJECT_ROOT / "postgres" / "generated" / "load_seed.sql"

TEST_DB = "retailpulse_phase1_test"


pytestmark = pytest.mark.skipif(
    os.getenv("RUN_POSTGRES_INTEGRATION") != "1",
    reason="Set RUN_POSTGRES_INTEGRATION=1 to run local PostgreSQL integration tests.",
)


def run_psql(database: str, sql: str) -> str:
    result = subprocess.run(
        [
            "docker",
            "compose",
            "exec",
            "-T",
            "postgres",
            "psql",
            "-U",
            "retailpulse",
            "-d",
            database,
            "-At",
            "-v",
            "ON_ERROR_STOP=1",
        ],
        input=sql,
        encoding="utf-8",
        capture_output=True,
        cwd=PROJECT_ROOT,
        check=True,
    )
    return result.stdout.strip()


def test_postgres_schema_seed_and_queries() -> None:
    run_psql(
        "retailpulse",
        f'DROP DATABASE IF EXISTS {TEST_DB}; CREATE DATABASE {TEST_DB};',
    )

    try:
        schema_sql = SCHEMA_PATH.read_text(encoding="utf-8-sig")
        run_psql(TEST_DB, schema_sql)

        load_seed_sql = LOAD_SEED_PATH.read_text(encoding="utf-8-sig")
        run_psql(TEST_DB, load_seed_sql)

        counts = run_psql(
            TEST_DB,
            """
            SELECT
                (SELECT COUNT(*) FROM customers),
                (SELECT COUNT(*) FROM inventory),
                (SELECT COUNT(*) FROM orders),
                (SELECT COUNT(*) FROM order_items);
            """,
        )

        customer_count, inventory_count, order_count, order_item_count = map(
            int,
            counts.split("|"),
        )

        assert customer_count == 100
        assert inventory_count == 50
        assert order_count == 500
        assert order_item_count > 0

        mismatched_totals = run_psql(
            TEST_DB,
            """
            SELECT COUNT(*)
            FROM (
                SELECT o.order_id
                FROM orders o
                JOIN order_items oi ON oi.order_id = o.order_id
                GROUP BY o.order_id, o.order_total
                HAVING o.order_total <> SUM(oi.quantity * oi.unit_price)
            ) AS mismatches;
            """,
        )

        assert int(mismatched_totals) == 0

    finally:
        run_psql(
            "retailpulse",
            (
                f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
                f"WHERE datname = '{TEST_DB}' AND pid <> pg_backend_pid(); "
                f"DROP DATABASE IF EXISTS {TEST_DB};"
            ),
        )
