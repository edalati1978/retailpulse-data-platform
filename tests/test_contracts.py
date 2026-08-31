from pathlib import Path

import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONTRACTS_DIR = PROJECT_ROOT / "docs" / "data-contracts"

CONTRACT_FILES = (
    "events.yaml",
    "open-meteo.yaml",
    "postgres-oltp.yaml",
    "tpcds.yaml",
)

REQUIRED_SECTIONS = {
    "contract_version",
    "source",
    "entity",
    "keys",
    "schema",
    "timestamps",
    "schema_versioning",
    "delivery",
    "quality",
    "failure_and_recovery",
    "security",
    "metadata",
    "samples",
    "limitations",
}


def load_contract(filename: str) -> dict:
    path = CONTRACTS_DIR / filename
    return yaml.safe_load(path.read_text(encoding="utf-8-sig"))


@pytest.mark.parametrize("filename", CONTRACT_FILES)
def test_contract_has_required_sections(filename: str) -> None:
    contract = load_contract(filename)

    assert REQUIRED_SECTIONS.issubset(contract)
    assert contract["contract_version"]
    assert contract["source"]["name"]
    assert contract["source"]["type"]
    assert contract["entity"]["name"]
    assert contract["entity"]["grain"]
    assert contract["schema_versioning"]["current_version"]


@pytest.mark.parametrize("filename", CONTRACT_FILES)
def test_contract_sample_path_exists(filename: str) -> None:
    contract = load_contract(filename)
    sample_path = PROJECT_ROOT / contract["samples"]["sample_file"]

    assert sample_path.exists()


@pytest.mark.parametrize("filename", CONTRACT_FILES)
def test_required_fields_exist_in_declared_schema(filename: str) -> None:
    contract = load_contract(filename)
    fields = contract["schema"]["fields"]
    required_fields = contract["quality"]["required_fields"]

    if not fields:
        return

    declared_names = {field["name"] for field in fields}

    assert set(required_fields).issubset(declared_names)
