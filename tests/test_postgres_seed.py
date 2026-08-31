import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SEED_SCRIPT = PROJECT_ROOT / "postgres" / "seed.py"

GENERATED_FILES = (
    "customers.csv",
    "inventory.csv",
    "orders.csv",
    "order_items.csv",
    "load_seed.sql",
)


def run_seed(output_dir: Path) -> None:
    subprocess.run(
        [
            sys.executable,
            str(SEED_SCRIPT),
            "--seed",
            "42",
            "--customers",
            "20",
            "--products",
            "10",
            "--orders",
            "30",
            "--output-dir",
            str(output_dir),
        ],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def test_seed_generation_is_deterministic(tmp_path: Path) -> None:
    first_output = tmp_path / "first"
    second_output = tmp_path / "second"

    run_seed(first_output)
    run_seed(second_output)

    for filename in GENERATED_FILES:
        first_file = first_output / filename
        second_file = second_output / filename

        assert first_file.exists()
        assert second_file.exists()
        assert first_file.read_bytes() == second_file.read_bytes()
