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
EXPECTED_FIELD_COUNTS = {
    "catalog_returns.sample.dat": 27,
    "catalog_sales.sample.dat": 34,
    "customer.sample.dat": 18,
    "inventory.sample.dat": 4,
    "store_returns.sample.dat": 20,
    "store_sales.sample.dat": 23,
    "web_returns.sample.dat": 24,
    "web_sales.sample.dat": 34,
}


def test_tpcds_sample_schema_shape() -> None:
    for filename, expected_fields in EXPECTED_FIELD_COUNTS.items():
        path = SAMPLES_DIR / filename

        with path.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                if not line.strip():
                    continue

                fields = line.rstrip("\r\n").split("|")

                if fields[-1] == "":
                    fields.pop()

                assert len(fields) == expected_fields, (
                    f"{filename}:{line_number} has {len(fields)} fields; "
                    f"expected {expected_fields}"
                )
