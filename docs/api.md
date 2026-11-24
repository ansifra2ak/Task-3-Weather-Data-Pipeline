# API integration reference

## Current weather (required provider)
`GET https://api.openweathermap.org/data/2.5/weather`

Query parameters: `lat`, `lon`, `appid` (your local secret), `units=metric`. Example non-executable placeholder request: `/data/2.5/weather?lat=17.385&lon=78.487&units=metric&appid=YOUR_KEY`.

JSON mapping: `dt` Unix time UTC; `main.temp` °C; `main.humidity` percent; `main.pressure` hPa; `wind.speed` m/s; `rain.1h` preceding hour mm if supplied; `weather[0].description` text. The pipeline tracks provider observation time, not script execution time. Repeated observation timestamps do not create duplicates.

## Historical archive (supplementary)
`GET https://archive-api.open-meteo.com/v1/archive`

Example: `?latitude=17.385&longitude=78.487&start_date=2025-01-01&end_date=2025-01-02&hourly=temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,rain,weather_code&timezone=GMT&wind_speed_unit=ms&models=era5`.

Hourly arrays are aligned by timestamp; temperature °C, humidity %, mean sea-level pressure hPa, wind m/s, rain mm, condition WMO code. ERA5 is reanalysis rather than station observations. Six-day lag is a conservative design choice; availability may vary. No API key is normally required for non-commercial public archive access, subject to provider terms.

## Failure handling
HTTPS, explicit timeout, bounded retries for network failures, 429 and 5xx. 401/403 require checking credentials or account access. HTTP status errors are redacted; never print a request URL with `appid`. Missing required fields and invalid measurements fail validation or mark the city extraction as unsuccessful. Partial successes are retained. See `pipeline_runs.csv` and logs for diagnostics.
