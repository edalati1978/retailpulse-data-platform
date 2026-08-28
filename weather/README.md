# Open-Meteo Weather Source

## Purpose

Open-Meteo is the selected weather source for RetailPulse weather enrichment.

The source will later be used to associate retail activity with daily weather conditions
for analysis such as the relationship between extreme temperature or precipitation
and order cancellation or fulfillment delays.

## API Endpoint

Historical Weather API:

`https://archive-api.open-meteo.com/v1/archive`

## Required Request Parameters

| Parameter | Meaning | Source |
|---|---|---|
| latitude | Geographic latitude | Open-Meteo documentation |
| longitude | Geographic longitude | Open-Meteo documentation |
| start_date | Start of requested historical period | Open-Meteo documentation |
| end_date | End of requested historical period | Open-Meteo documentation |
| daily | Requested daily weather variables | Open-Meteo documentation |
| timezone | Time zone used for daily aggregation | Open-Meteo documentation |

## Selected Daily Variables

| Open-Meteo Field | Meaning | Unit | RetailPulse Use |
|---|---|---|---|
| temperature_2m_max | Maximum daily air temperature at 2 meters | °C | Identify extreme heat |
| temperature_2m_min | Minimum daily air temperature at 2 meters | °C | Identify extreme cold |
| precipitation_sum | Total daily precipitation | mm | Analyze rain-related operational impact |
| weather_code | Daily WMO weather condition code | WMO code | Categorize general weather conditions |

## Selection Rationale

The RetailPulse project needs weather enrichment mainly to investigate whether
temperature extremes and precipitation are associated with operational outcomes
such as cancellations or fulfillment delays.

Many additional Open-Meteo variables are available, but they are intentionally
excluded unless a later business requirement justifies them.

## Data Grain

One logical weather record represents:

`one location + one calendar date`
## Client Behavior

The reusable `OpenMeteoClient` is implemented in `weather/open_meteo_client.py`.

### Timeout

Each HTTP request uses a configurable timeout.

Default:

`10 seconds`

### Retry

The client retries temporary failures:

- request timeout
- connection failure
- HTTP 429
- HTTP 500
- HTTP 502
- HTTP 503
- HTTP 504

The default configuration allows:

`1 initial attempt + up to 2 retries`

Retry delay uses bounded exponential backoff.

Non-retryable HTTP errors fail immediately.

### Cache

Successful responses are cached locally under:

`weather/cache/`

The cache key is based on:

`daily + latitude + longitude + start_date + end_date`

If the expected cache file already exists, the client returns the cached response
without calling the Open-Meteo API.

Runtime cache files are excluded from Git and are intended for local development
and small-scale use.