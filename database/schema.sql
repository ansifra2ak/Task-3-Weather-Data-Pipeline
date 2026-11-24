PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS cities (
 id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, country TEXT NOT NULL DEFAULT 'IN',
 latitude REAL NOT NULL, longitude REAL NOT NULL, timezone TEXT NOT NULL DEFAULT 'Asia/Kolkata');
CREATE TABLE IF NOT EXISTS sources (id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, kind TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS pipeline_runs (
 id INTEGER PRIMARY KEY, source_id INTEGER NOT NULL REFERENCES sources(id), started TEXT NOT NULL,
 finished TEXT, status TEXT NOT NULL, expected INTEGER NOT NULL DEFAULT 0, received INTEGER NOT NULL DEFAULT 0,
 inserted INTEGER NOT NULL DEFAULT 0, rejected INTEGER NOT NULL DEFAULT 0, error TEXT);
CREATE TABLE IF NOT EXISTS weather_data (
 id INTEGER PRIMARY KEY, city_id INTEGER NOT NULL REFERENCES cities(id), source_id INTEGER NOT NULL REFERENCES sources(id),
 observed_at TEXT NOT NULL, temperature_c REAL NOT NULL CHECK(temperature_c BETWEEN -90 AND 65),
 humidity REAL NOT NULL CHECK(humidity BETWEEN 0 AND 100), pressure_hpa REAL NOT NULL CHECK(pressure_hpa BETWEEN 300 AND 1100),
 wind_mps REAL NOT NULL CHECK(wind_mps >= 0), rain_mm REAL NOT NULL CHECK(rain_mm >= 0), condition TEXT NOT NULL,
 UNIQUE(city_id,source_id,observed_at));
CREATE TABLE IF NOT EXISTS alerts (
 id INTEGER PRIMARY KEY, weather_id INTEGER NOT NULL REFERENCES weather_data(id), metric TEXT NOT NULL,
 value REAL NOT NULL, threshold REAL NOT NULL, created TEXT NOT NULL, UNIQUE(weather_id,metric));
CREATE INDEX IF NOT EXISTS idx_weather_source_time ON weather_data(source_id,observed_at);
CREATE INDEX IF NOT EXISTS idx_weather_city_time ON weather_data(city_id,observed_at);
