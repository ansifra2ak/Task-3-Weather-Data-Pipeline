# Operations and testing

## Setup / deployment
Local deployment only. Python 3.10+, network access, installation permissions, activated OpenWeatherMap key. Use `run.py`. Configuration is in `config/settings.py`; change intervals and thresholds before starting. Run the dashboard on localhost; do not expose it publicly without authentication/security review. The scheduler runs only while launcher and computer are running. It collects live data hourly, regenerates reports and makes a daily backup after a scheduled run. To stop, Ctrl+C. For a production service use a managed process supervisor; not required for the advanced local version.

## Troubleshooting
- HTTP 401: check key activation, account, spelling; replace local `.env` or environment variable and restart.
- HTTP 429: wait for provider quota to reset, lower call rate; do not repeatedly launch.
- No archive rows: inspect connectivity/availability and `reports/pipeline_runs.csv`; rerun history when provider is available.
- Dashboard empty: check run status and data counts. Do not present empty charts as results.
- Port in use: stop old Streamlit instance or use `.venv/bin/python -m streamlit run dashboard/app.py --server.port 8502`.
- Package install error: verify Python and network, select supported Python interpreter, recreate `.venv` if necessary.
- Stale live records: keep Mac awake and check scheduler logs; dashboard refresh is manual.

## Test plan
`pytest` covers validation, API parsing, duplicate prevention, alert thresholds, failed runs, rejected data, historical SQL analytics/report generation, backups, foreign keys and secret redaction. Tests use temporary databases and labeled mock data, never the production database. The launcher writes actual local results to `reports/test_results.txt`.

## Backup and restoration
Use `.venv/bin/python main.py backup` for an online SQLite backup. Stop the application and scheduler before restoring. Preserve the current database as a separate backup; remove stale `weather_data.db-wal` and `weather_data.db-shm` only after the application is fully stopped. Copy the selected backup to `database/weather_data.db`. Restart and verify integrity and coverage. Never delete your only backup.

## Evidence
Capture screenshots of live weather, historical charts, alerts, pipeline health and actual test output. Store in `screenshots/`. Record data coverage and any limitations in the report before submission.
