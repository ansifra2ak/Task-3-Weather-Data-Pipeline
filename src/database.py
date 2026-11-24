"""SQLite connections, schema, transactions, and safe backups."""
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from config.settings import ROOT, DB, CITIES, THRESHOLDS

def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')

@contextmanager
def connect(path=DB):
    conn = sqlite3.connect(path, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys=ON')
    try:
        with conn:
            yield conn
    finally:
        conn.close()

def setup(path=DB):
    with connect(path) as c:
        c.execute('PRAGMA journal_mode=WAL')
        c.executescript((ROOT/'database/schema.sql').read_text())
        c.executemany('INSERT OR IGNORE INTO cities(name,latitude,longitude) VALUES(?,?,?)', CITIES)
        c.executemany('INSERT OR IGNORE INTO sources(name,kind) VALUES(?,?)', [('OpenWeatherMap','current API'),('Open-Meteo','historical reanalysis')])

def start_run(source, expected, path=DB):
    with connect(path) as c:
        sid = c.execute('SELECT id FROM sources WHERE name=?',(source,)).fetchone()[0]
        return c.execute('INSERT INTO pipeline_runs(source_id,started,status,expected) VALUES(?,?,?,?)',(sid,now(),'running',expected)).lastrowid

def finish_run(run, status, received, inserted, rejected, error='', path=DB):
    with connect(path) as c:
        c.execute('UPDATE pipeline_runs SET finished=?,status=?,received=?,inserted=?,rejected=?,error=? WHERE id=?', (now(),status,received,inserted,rejected,error[:2000],run))

def store(city, source, rows, path=DB):
    count=0
    with connect(path) as c:
        cid=c.execute('SELECT id FROM cities WHERE name=?',(city,)).fetchone()[0]
        sid=c.execute('SELECT id FROM sources WHERE name=?',(source,)).fetchone()[0]
        for r in rows:
            cur=c.execute('INSERT OR IGNORE INTO weather_data(city_id,source_id,observed_at,temperature_c,humidity,pressure_hpa,wind_mps,rain_mm,condition) VALUES(?,?,?,?,?,?,?,?,?)',(cid,sid,*r))
            if cur.rowcount:
                count+=1
                if source=='OpenWeatherMap':
                    for metric, value in zip(('temperature_c','humidity','rain_mm'),(r[1],r[2],r[5])):
                        if value>=THRESHOLDS[metric]:
                            c.execute('INSERT INTO alerts(weather_id,metric,value,threshold,created) VALUES(?,?,?,?,?)',(cur.lastrowid,metric,value,THRESHOLDS[metric],now()))
    return count

def backup(path=DB, dest=None):
    dest=dest or ROOT/'database/backups'/f"weather_{datetime.now():%Y%m%d_%H%M%S}.db"
    dest.parent.mkdir(parents=True, exist_ok=True)
    with connect(path) as c:
        target=sqlite3.connect(dest)
        try: c.backup(target)
        finally: target.close()
    return dest
