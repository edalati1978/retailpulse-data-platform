from pathlib import Path

SAMPLES_DIR = Path(__file__).resolve().parents[1] / "tpcds" / "samples"

EXPECTED_SAMPLE_FILES = [
    "catalog_returns.sample.dat",
    "catalog_sales.sample.dat",
    "customer.sample.dat",
    "inventory.sample.dat",
    "store_returns.sample.dat",
    "store_sales.sample.dat",
    "web_returns.sample.dat",
    "web_sales.sample.dat",
]


def test_required_tpcds_sample_files_exist() -> None:
    for filename in EXPECTED_SAMPLE_FILES:
        assert (SAMPLES_DIR / filename).is_file(), f"Missing TPC-DS sample: {filename}"


def test_tpcds_sample_files_have_five_rows() -> None:
    for filename in EXPECTED_SAMPLE_FILES:
        path = SAMPLES_DIR / filename
        with path.open("r", encoding="utf-8") as file:
            row_count = sum(1 for line in file if line.strip())

        assert row_count == 5, f"{filename} has {row_count} rows; expected 5"