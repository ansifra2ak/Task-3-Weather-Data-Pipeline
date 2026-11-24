"""HTTPS clients, bounded retries and redacted error messages."""
import os, time
from datetime import datetime, timezone
import requests
from config.settings import ROOT

LIVE='https://api.openweathermap.org/data/2.5/weather'
ARCHIVE='https://archive-api.open-meteo.com/v1/archive'
FIELDS='temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,rain,weather_code'

def api_key():
    if os.environ.get('OPENWEATHER_API_KEY'): return os.environ['OPENWEATHER_API_KEY'].strip()
    p=ROOT/'.env'
    if p.exists():
        for line in p.read_text().splitlines():
            if line.startswith('OPENWEATHER_API_KEY='): return line.split('=',1)[1].strip()
    return ''

def fetch(url, params):
    for attempt in range(3):
        try:
            r=requests.get(url, params=params, timeout=(10,60))
            if r.status_code==429 or r.status_code>=500:
                if attempt<2:
                    delay=r.headers.get('Retry-After','')
                    time.sleep(min(int(delay),30) if delay.isdigit() else 2**attempt)
                    continue
            if not r.ok: raise RuntimeError(f'HTTP {r.status_code} from weather provider')
            return r.json()
        except (requests.RequestException, ValueError):
            if attempt==2: raise RuntimeError('Weather provider connection or JSON error') from None
            time.sleep(2**attempt)
    raise RuntimeError('Weather provider unavailable')

def parse_live(d):
    return (datetime.fromtimestamp(d['dt'],timezone.utc).isoformat(),d['main']['temp'],d['main']['humidity'],d['main']['pressure'],d['wind']['speed'],d.get('rain',{}).get('1h',0),d['weather'][0]['description'])

def live(city,key):
    _,lat,lon=city
    return parse_live(fetch(LIVE,{'lat':lat,'lon':lon,'appid':key,'units':'metric'}))

def archive(city,start,end):
    _,lat,lon=city
    d=fetch(ARCHIVE,{'latitude':lat,'longitude':lon,'start_date':str(start),'end_date':str(end),'hourly':FIELDS,'timezone':'GMT','wind_speed_unit':'ms','models':'era5'})
    h=d['hourly']
    fields=FIELDS.split(',')
    if any(len(h[f])!=len(h['time']) for f in fields): raise RuntimeError('Incomplete archive arrays')
    return [(t+'+00:00',*(h[f][i] for f in fields[:-1]),f"WMO {h['weather_code'][i]}" if h['weather_code'][i] is not None else '') for i,t in enumerate(h['time'])]
