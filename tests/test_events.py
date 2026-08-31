import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker, ValidationError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PROJECT_ROOT / "streaming" / "event.schema.json"
VALID_EVENT_PATH = PROJECT_ROOT / "streaming" / "sample_valid_event.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def event_validator() -> Draft202012Validator:
    schema = load_json(SCHEMA_PATH)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def test_valid_event_passes_schema_validation() -> None:
    event = load_json(VALID_EVENT_PATH)

    event_validator().validate(event)


def test_event_without_event_id_is_rejected() -> None:
    event = copy.deepcopy(load_json(VALID_EVENT_PATH))
    event.pop("event_id")

    with pytest.raises(ValidationError) as exc_info:
        event_validator().validate(event)

    assert exc_info.value.validator == "required"
    assert "event_id" in exc_info.value.validator_value


def test_event_with_unsupported_schema_version_is_rejected() -> None:
    event = copy.deepcopy(load_json(VALID_EVENT_PATH))
    event["schema_version"] = "2.0.0"

    with pytest.raises(ValidationError) as exc_info:
        event_validator().validate(event)

    assert exc_info.value.validator == "const"
    assert exc_info.value.validator_value == "1.0.0"
