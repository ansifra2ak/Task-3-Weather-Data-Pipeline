# Architecture and relational schema

```mermaid
flowchart TD
 A[OpenWeatherMap current API] --> C[ETL extraction]
 B[Open-Meteo ERA5 archive] --> C
 C --> D[Validation and UTC normalization]
 D --> E[(SQLite)]
 D --> F[Run logs and audit]
 E --> G[SQL analytics]
 E --> H[Threshold alerts]
 G --> I[CSV and Markdown reports]
 G --> J[Streamlit dashboard]
 H --> J
 F --> J
 K[Hourly scheduler] --> C
 E --> L[SQLite backup]
```

```mermaid
erDiagram
 CITIES ||--o{ WEATHER_DATA : has
 SOURCES ||--o{ WEATHER_DATA : provides
 SOURCES ||--o{ PIPELINE_RUNS : audits
 WEATHER_DATA ||--o{ ALERTS : triggers
 CITIES {
  int id PK
 string name UK
 string country
 float latitude
 float longitude
 string timezone
 }
 SOURCES {
  int id PK
 string name UK
 string kind
 }
 WEATHER_DATA {
  int id PK
 int city_id FK
 int source_id FK
 string observed_at
 float temperature_c
 float humidity
 float pressure_hpa
 float wind_mps
 float rain_mm
 string condition
 }
 PIPELINE_RUNS {
  int id PK
 int source_id FK
 string started
 string finished
 string status
 int expected
 int received
 int inserted
 int rejected
 string error
 }
 ALERTS {
  int id PK
 int weather_id FK
 string metric
 float value
 float threshold
 string created
 }
```

Five tables separate location identity, data provenance, measurements, ETL audit and alerts. The compound unique key `(city_id, source_id, observed_at)` prevents repeated imports. Each non-key measurement is tied to a single source/city/time observation. Foreign keys are enabled on every connection; WAL and transactions protect writes. See `database/schema.sql` for executable DDL. UTC ISO timestamps are normalized before insertion; analytics convert to IST. API retry is bounded; invalid data is rejected, not replaced with zero (except absent live rain, interpreted as no reported rain in the provider response). Pipeline expected/received/inserted/rejected counts distinguish failed extraction and duplicate rows. Audit records do not link each observation to a run; this is a local project limitation.

SQL implementations in `src/analytics.py` cover JOIN, GROUP BY, AVG, COUNT, CASE, date functions, CTE and ROW_NUMBER. Pearson correlation is calculated in pandas on SQL-extracted matched hourly rows. All historical comparisons use only ERA5 data to avoid mixing source methodologies.
