import json

import pytest
import requests

from weather.open_meteo_client import OpenMeteoClient


def test_build_params() -> None:
    client = OpenMeteoClient()

    params = client.build_params(
        latitude=47.6062,
        longitude=-122.3321,
        start_date="2025-01-01",
        end_date="2025-01-02",
    )

    assert params["latitude"] == 47.6062
    assert params["longitude"] == -122.3321
    assert params["start_date"] == "2025-01-01"
    assert params["end_date"] == "2025-01-02"
    assert params["timezone"] == "UTC"
    assert params["daily"] == (
        "temperature_2m_max,"
        "temperature_2m_min,"
        "precipitation_sum,"
        "weather_code"
    )


def test_fetch_weather_uses_cache(tmp_path, monkeypatch) -> None:
    client = OpenMeteoClient(cache_dir=str(tmp_path))

    cache_path = client._cache_path(
        latitude=47.6062,
        longitude=-122.3321,
        start_date="2025-01-01",
        end_date="2025-01-01",
    )

    expected_data = {
        "daily": {
            "time": ["2025-01-01"],
            "temperature_2m_max": [10.0],
        }
    }

    cache_path.write_text(
        json.dumps(expected_data),
        encoding="utf-8",
    )

    def fail_if_api_is_called(*args, **kwargs):
        raise AssertionError("API should not be called when cache exists")

    monkeypatch.setattr(
        "weather.open_meteo_client.requests.get",
        fail_if_api_is_called,
    )

    actual_data = client.fetch_weather(
        latitude=47.6062,
        longitude=-122.3321,
        start_date="2025-01-01",
        end_date="2025-01-01",
    )

    assert actual_data == expected_data


def test_request_retries_after_retryable_error(monkeypatch) -> None:
    client = OpenMeteoClient(
        max_retries=2,
        retry_delay_seconds=0,
    )

    call_count = 0

    expected_data = {
        "daily": {
            "time": ["2025-01-01"],
        }
    }

    class FakeResponse:
        def __init__(self, status_code, data=None):
            self.status_code = status_code
            self._data = data

        def raise_for_status(self):
            pass

        def json(self):
            return self._data

    def fake_get(*args, **kwargs):
        nonlocal call_count
        call_count += 1

        if call_count == 1:
            return FakeResponse(500)

        return FakeResponse(200, expected_data)

    monkeypatch.setattr(
        "weather.open_meteo_client.requests.get",
        fake_get,
    )

    result = client._request_with_retry(
        {
            "latitude": 47.6062,
            "longitude": -122.3321,
        }
    )

    assert call_count == 2
    assert result == expected_data
def test_fetch_weather_calls_api_and_writes_cache(tmp_path, monkeypatch) -> None:
    client = OpenMeteoClient(
        cache_dir=str(tmp_path),
        retry_delay_seconds=0,
    )

    expected_data = {
        "daily": {
            "time": ["2025-01-01"],
            "temperature_2m_max": [10.0],
        }
    }

    class FakeResponse:
        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):
            return expected_data

    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(
        "weather.open_meteo_client.requests.get",
        fake_get,
    )

    actual_data = client.fetch_weather(
        latitude=47.6062,
        longitude=-122.3321,
        start_date="2025-01-01",
        end_date="2025-01-01",
    )

    cache_path = client._cache_path(
        latitude=47.6062,
        longitude=-122.3321,
        start_date="2025-01-01",
        end_date="2025-01-01",
    )

    assert actual_data == expected_data
    assert cache_path.exists()
    assert json.loads(cache_path.read_text(encoding="utf-8")) == expected_data    
def test_request_does_not_retry_non_retryable_error(monkeypatch) -> None:
    client = OpenMeteoClient(
        max_retries=2,
        retry_delay_seconds=0,
    )

    call_count = 0

    def fake_get(*args, **kwargs):
        nonlocal call_count
        call_count += 1

        response = requests.Response()
        response.status_code = 400
        response.url = "https://archive-api.open-meteo.com/v1/archive"
        return response

    monkeypatch.setattr(
        "weather.open_meteo_client.requests.get",
        fake_get,
    )

    with pytest.raises(requests.HTTPError):
        client._request_with_retry(
            {
                "latitude": 47.6062,
                "longitude": -122.3321,
            }
        )

    assert call_count == 1    