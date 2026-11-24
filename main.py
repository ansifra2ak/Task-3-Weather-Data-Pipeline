"""CLI entry point for all project operations."""
import argparse, getpass, subprocess, sys
from datetime import datetime,timezone,timedelta
from config.settings import ROOT,DB,ARCHIVE_LAG_DAYS,HISTORY_DAYS
from src import database as db, api_client as api
from src.etl_pipeline import run
from src.reporter import generate

def bootstrap():
    db.setup()
    if not api.api_key():
        key=getpass.getpass('Paste OpenWeatherMap API key (hidden; Enter to skip): ').strip()
        if key:
            if not key.isalnum(): raise SystemExit('Invalid key format. Try again.')
            p=ROOT/'.env'; p.write_text('OPENWEATHER_API_KEY='+key+'\n'); p.chmod(0o600)
    with db.connect() as c:
        end=datetime.now(timezone.utc).date()-timedelta(days=ARCHIVE_LAG_DAYS)
        start=end-timedelta(days=HISTORY_DAYS-1)
        coverage=c.execute("SELECT COUNT(*) FROM weather_data w JOIN sources s ON s.id=w.source_id WHERE s.name='Open-Meteo' AND date(observed_at) BETWEEN ? AND ?",(str(start),str(end))).fetchone()[0]
    if coverage < 15*HISTORY_DAYS*24: print('Historical import:',run('Open-Meteo'),flush=True)
    if api.api_key(): print('Live collection:',run('OpenWeatherMap'),flush=True)
    else: print('Live collection skipped: API key not configured.')
    print('Report:',generate(),flush=True)
    db.backup()
    test=subprocess.run([sys.executable,'-m','pytest','-q'],cwd=ROOT,capture_output=True,text=True)
    (ROOT/'reports/test_results.txt').write_text(test.stdout+test.stderr)
    print(test.stdout,flush=True)
    if test.returncode: raise SystemExit('Tests failed; see reports/test_results.txt')
    scheduler=subprocess.Popen([sys.executable,'main.py','schedule'],cwd=ROOT) if api.api_key() else None
    try:
        subprocess.run([sys.executable,'-m','streamlit','run','dashboard/app.py','--server.address','127.0.0.1'],cwd=ROOT,check=True)
    finally:
        if scheduler:
            scheduler.terminate(); scheduler.wait(timeout=10)

def main():
    p=argparse.ArgumentParser(); p.add_argument('action',nargs='?',default='start',choices=['start','init','live','history','report','schedule','backup']); a=p.parse_args().action
    db.setup()
    if a=='start': bootstrap()
    elif a=='live':
        if not api.api_key(): raise SystemExit('Configure OPENWEATHER_API_KEY in .env first.')
        print(run('OpenWeatherMap')); generate()
    elif a=='history': print(run('Open-Meteo')); generate()
    elif a=='report': print(generate())
    elif a=='backup': print(db.backup())
    elif a=='schedule':
        from src.scheduler import serve
        serve()

if __name__=='__main__': main()
