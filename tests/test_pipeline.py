from datetime import datetime,timezone,date,timedelta
import pytest
from src import database as db, api_client as api
from src.validators import validate
from src.etl_pipeline import run
from src.analytics import results,current,alerts
from src.reporter import generate
from src.monitor import health
from config.settings import CITIES

@pytest.fixture
def path(tmp_path):
    p=tmp_path/'test.db'; db.setup(p); return p

def row(temp=42,humidity=95,rain=25):
    return (datetime.now(timezone.utc).isoformat(),temp,humidity,1010,2,rain,'test fixture')

def test_validation():
    assert validate(row())[1]==42
    for r in [row(humidity=101),row(temp=float('nan')),row(rain=-1),row(temp=None)]:
        with pytest.raises((ValueError,TypeError)): validate(r)

def test_live_parser():
    d={'dt':1700000000,'main':{'temp':29,'humidity':50,'pressure':1000},'wind':{'speed':2},'weather':[{'description':'clear'}]}
    assert api.parse_live(d)[5]==0

def test_pipeline_and_duplicates(path):
    r=row(); kwargs={'path':path,'cities':CITIES[:1],'extractor':lambda _: [r]}
    assert run('OpenWeatherMap',**kwargs)['inserted']==1
    assert run('OpenWeatherMap',**kwargs)['inserted']==0
    assert len(current(path))==1 and len(alerts(path))==3
    assert health(path)[0]=='success'

def test_failed_run(path):
    def fail(_): raise RuntimeError('HTTP 401 from weather provider')
    assert run('OpenWeatherMap',path=path,cities=CITIES[:1],extractor=fail)['status']=='failed'
    assert health(path)[0]=='failed'

def test_quality_rejection(path):
    r=run('OpenWeatherMap',path=path,cities=CITIES[:1],extractor=lambda _: [row(humidity=120)])
    assert r['rejected']==1 and r['status']=='failed' and current(path).empty

def test_archive_analytics_and_report(path,tmp_path):
    day=date.today()-timedelta(days=10)
    rows=[(f'{day}T{i:02}:00:00+00:00',20+i,50+i,1000,3,i,'WMO 0') for i in range(24)]
    assert run('Open-Meteo',path=path,cities=CITIES[:1],extractor=lambda _:rows,start=day,end=day)['status']=='success'
    data=results(path)
    assert all(not d.empty for d in data.values())
    assert data['humidity_rain_correlation'].iloc[0].pearson_r==pytest.approx(1)
    assert generate(path,tmp_path/'reports').exists()
    assert current(path).empty

def test_backup_and_foreign_keys(path,tmp_path):
    import sqlite3
    with pytest.raises(sqlite3.IntegrityError):
        with db.connect(path) as c: c.execute("INSERT INTO pipeline_runs(source_id,started,status) VALUES(999,'x','running')")
    copy=db.backup(path,tmp_path/'backup.db')
    assert health(copy)[-1]=='ok'

def test_http_key_not_leaked(monkeypatch):
    import requests
    def fail(*a,**k): raise requests.ConnectionError('secret_key')
    monkeypatch.setattr(api.requests,'get',fail); monkeypatch.setattr(api.time,'sleep',lambda _:None)
    with pytest.raises(RuntimeError) as e: api.fetch(api.LIVE,{'appid':'secret_key'})
    assert 'secret_key' not in str(e.value)
