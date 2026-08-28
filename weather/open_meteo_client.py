from __future__ import annotations

import json
import time
from pathlib import Path

import requests

OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

DEFAULT_DAILY_VARIABLES = (
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "weather_code",
)

RETRYABLE_STATUS_CODES = {
    429,
    500,
    502,
    503,
    504,
}


class OpenMeteoClient:
    def __init__(
        self,
        timeout_seconds: int = 10,
        max_retries: int = 2,
        retry_delay_seconds: float = 1.0,
        cache_dir: str = "weather/cache",
    ) -> None:
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.retry_delay_seconds = retry_delay_seconds
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def build_params(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
    ) -> dict[str, str | float]:
        return {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "daily": ",".join(DEFAULT_DAILY_VARIABLES),
            "timezone": "UTC",
        }

    def _cache_path(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
    ) -> Path:
        filename = f"daily_{latitude}_{longitude}_{start_date}_{end_date}.json"
        return self.cache_dir / filename

    def _request_with_retry(
        self,
        params: dict[str, str | float],
    ) -> dict:
        for attempt in range(self.max_retries + 1):
            try:
                response = requests.get(
                    OPEN_METEO_ARCHIVE_URL,
                    params=params,
                    timeout=self.timeout_seconds,
                )

                if response.status_code in RETRYABLE_STATUS_CODES:
                    if attempt == self.max_retries:
                        response.raise_for_status()

                    time.sleep(
                        self.retry_delay_seconds * (2**attempt)
                    )
                    continue

                response.raise_for_status()
                return response.json()

            except (requests.Timeout, requests.ConnectionError):
                if attempt == self.max_retries:
                    raise

                time.sleep(
                    self.retry_delay_seconds * (2**attempt)
                )

        raise RuntimeError("Open-Meteo request failed unexpectedly.")

    def fetch_weather(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
    ) -> dict:
        cache_path = self._cache_path(
            latitude,
            longitude,
            start_date,
            end_date,
        )

        if cache_path.exists():
            return json.loads(
                cache_path.read_text(encoding="utf-8")
            )

        params = self.build_params(
            latitude=latitude,
            longitude=longitude,
            start_date=start_date,
            end_date=end_date,
        )

        data = self._request_with_retry(params)

        cache_path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

        return data