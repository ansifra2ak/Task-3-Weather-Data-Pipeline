"""SQL joins, aggregations, CTEs and window functions; source-aware analytics."""
import pandas as pd
from config.settings import DB
from src.database import connect
BASE="""FROM weather_data w JOIN cities c ON c.id=w.city_id JOIN sources s ON s.id=w.source_id"""
HIST=" WHERE s.name='Open-Meteo'"
LOCAL="datetime(w.observed_at,'+5 hours','+30 minutes')"

def query(sql, params=(), path=DB):
    with connect(path) as c: return pd.read_sql_query(sql,c,params=params)

def results(path=DB):
    city=query('SELECT c.name AS city, ROUND(AVG(w.temperature_c),2) AS avg_temp_c, COUNT(*) AS records '+BASE+HIST+' GROUP BY c.id ORDER BY avg_temp_c DESC',path=path)
    trend=query(f"SELECT date({LOCAL}) AS day,c.name AS city,ROUND(AVG(w.temperature_c),2) AS avg_temp_c,COUNT(*) AS hours "+BASE+HIST+f" AND date({LOCAL}) BETWEEN date('now','+5 hours','+30 minutes','-29 days') AND date('now','+5 hours','+30 minutes') GROUP BY day,c.id ORDER BY day",path=path)
    recent=query(f"SELECT date({LOCAL}) AS day,c.name AS city,ROUND(AVG(w.temperature_c),2) AS avg_temp_c,COUNT(*) AS hours "+BASE+HIST+f" AND date({LOCAL}) BETWEEN date((SELECT MAX(observed_at) FROM weather_data WHERE source_id=(SELECT id FROM sources WHERE name='Open-Meteo')),'+5 hours','+30 minutes','-29 days') AND date((SELECT MAX(observed_at) FROM weather_data WHERE source_id=(SELECT id FROM sources WHERE name='Open-Meteo')),'+5 hours','+30 minutes') GROUP BY day,c.id ORDER BY day",path=path)
    raw=query('SELECT c.name AS city,w.humidity,w.rain_mm '+BASE+HIST,path=path)
    correlations=[]
    for name,g in raw.groupby('city'):
        correlations.append({'city':name,'pearson_r':g.humidity.corr(g.rain_mm) if len(g)>1 and g.humidity.nunique()>1 and g.rain_mm.nunique()>1 else None,'paired_hours':len(g)})
    corr=pd.DataFrame(correlations,columns=['city','pearson_r','paired_hours'])
    season=f"CASE WHEN strftime('%m',{LOCAL}) IN ('12','01','02') THEN 'Winter' WHEN strftime('%m',{LOCAL}) IN ('03','04','05') THEN 'Pre-monsoon' WHEN strftime('%m',{LOCAL}) IN ('06','07','08','09') THEN 'Monsoon' ELSE 'Post-monsoon' END"
    seasonal=query(f"SELECT {season} AS season,COUNT(*) AS hours, SUM(CASE WHEN w.temperature_c>=40 OR w.temperature_c<=5 OR w.rain_mm>=20 THEN 1 ELSE 0 END) AS extreme_hours, ROUND(100.0*AVG(CASE WHEN w.temperature_c>=40 OR w.temperature_c<=5 OR w.rain_mm>=20 THEN 1.0 ELSE 0 END),2) AS extreme_pct,MAX(w.temperature_c) AS max_temp_c, MAX(w.rain_mm) AS max_rain_mm "+BASE+HIST+' GROUP BY season ORDER BY extreme_pct DESC',path=path)
    peak=query(f"WITH hourly AS (SELECT c.name AS city,strftime('%H',{LOCAL}) AS local_hour, AVG(w.temperature_c) AS avg_temp_c,COUNT(*) AS samples "+BASE+HIST+" GROUP BY c.id,local_hour), ranked AS (SELECT *,ROW_NUMBER() OVER(PARTITION BY city ORDER BY avg_temp_c DESC,local_hour) AS rn FROM hourly) SELECT city,local_hour,ROUND(avg_temp_c,2) AS avg_temp_c,samples FROM ranked WHERE rn=1 ORDER BY city",path=path)
    return {'city_averages':city,'last_30_days':trend,'latest_available_30_days':recent,'humidity_rain_correlation':corr,'seasonal_extremes':seasonal,'peak_hours_IST':peak}

def current(path=DB):
    return query('WITH ranked AS (SELECT c.name AS city,w.observed_at,w.temperature_c,w.humidity,w.pressure_hpa,w.wind_mps,w.rain_mm,w.condition,ROW_NUMBER() OVER(PARTITION BY c.id ORDER BY w.observed_at DESC) AS rn '+BASE+" WHERE s.name='OpenWeatherMap') SELECT * FROM ranked WHERE rn=1 ORDER BY city",path=path).drop(columns='rn')

def alerts(path=DB):
    return query('SELECT c.name AS city,w.observed_at,a.metric,a.value,a.threshold FROM alerts a JOIN weather_data w ON w.id=a.weather_id JOIN cities c ON c.id=w.city_id ORDER BY w.observed_at DESC LIMIT 100',path=path)
