from src.analytics import query
from config.settings import DB, INTERVAL_MINUTES
from datetime import datetime, timezone

def health(path=DB):
    runs=query('SELECT r.*,s.name AS source FROM pipeline_runs r JOIN sources s ON s.id=r.source_id ORDER BY r.id DESC LIMIT 30',path=path)
    live=query("SELECT r.* FROM pipeline_runs r JOIN sources s ON s.id=r.source_id WHERE s.name='OpenWeatherMap' ORDER BY r.id DESC LIMIT 1",path=path)
    status='No live runs'; age=None
    if not live.empty:
        r=live.iloc[0]; status=str(r.status)
        if r.finished:
            age=(datetime.now(timezone.utc)-datetime.fromisoformat(r.finished)).total_seconds()/60
            if age>INTERVAL_MINUTES*2: status='Stale'
        elif r.status=='running':
            age=(datetime.now(timezone.utc)-datetime.fromisoformat(r.started)).total_seconds()/60
            if age>INTERVAL_MINUTES*2: status='Stalled'
    counts=query('SELECT s.name AS source,COUNT(w.id) AS records,COUNT(DISTINCT w.city_id) AS cities,MIN(w.observed_at) AS first_record,MAX(w.observed_at) AS last_record FROM sources s LEFT JOIN weather_data w ON w.source_id=s.id GROUP BY s.id',path=path)
    integrity=query('PRAGMA quick_check',path=path).iloc[0,0]
    return status,age,counts,runs,integrity
