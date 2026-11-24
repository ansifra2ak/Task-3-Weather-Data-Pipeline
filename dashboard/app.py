import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import streamlit as st
import plotly.express as px
import pandas as pd
from src.analytics import results,current,alerts
from src.monitor import health
from src.database import setup
from config.settings import ROOT
st.set_page_config(page_title='Weather Intelligence',page_icon='🌦️',layout='wide')
setup()
st.title('Weather Intelligence | India')
st.caption('OpenWeatherMap live snapshots • Open-Meteo ERA5 historical reanalysis • local time IST')
if st.button('Refresh from database'): st.rerun()
status,age,counts,runs,integrity=health()
live=current(); data=results(); warnings=alerts()
a,b,c,d=st.columns(4)
a.metric('Pipeline status',status); b.metric('Stored records',f'{int(counts.records.sum()):,}'); c.metric('Live cities',len(live)); d.metric('Database',str(integrity))
if age is not None: st.caption(f'Last live run finished {age:.1f} minutes ago. Refresh to see new records.')
tabs=st.tabs(['Live weather','Historical analytics','Alerts','Pipeline health','Reports'])
with tabs[0]:
    if live.empty: st.warning('No live records. Check API key and pipeline logs.')
    else:
        live['observed_at']=pd.to_datetime(live.observed_at,utc=True).dt.tz_convert('Asia/Kolkata').astype(str)
        st.plotly_chart(px.bar(live,x='city',y='temperature_c',color='temperature_c',title='Latest temperature by city (°C)'),use_container_width=True)
        st.dataframe(live,use_container_width=True)
with tabs[1]:
    st.info('Historical ERA5 values are modeled estimates. Gaps are left blank; the latest archive dates may be delayed.')
    for name,df in data.items():
        st.subheader(name.replace('_',' ').title())
        if df.empty: st.warning('No historical data for this analysis.'); continue
        if name in ('last_30_days','latest_available_30_days'):
            st.plotly_chart(px.line(df,x='day',y='avg_temp_c',color='city',markers=True),use_container_width=True)
        elif name=='seasonal_extremes': st.plotly_chart(px.bar(df,x='season',y='extreme_pct'),use_container_width=True)
        elif name=='humidity_rain_correlation': st.plotly_chart(px.bar(df,x='city',y='pearson_r'),use_container_width=True)
        elif name=='city_averages': st.plotly_chart(px.bar(df,x='city',y='avg_temp_c'),use_container_width=True)
        st.dataframe(df,use_container_width=True)
    st.caption('Extreme hour: ≥40°C, ≤5°C, or ≥20 mm rain; rate normalized by sample count. Peak hours are IST hour buckets.')
with tabs[2]:
    st.caption('Project thresholds, not official meteorological warnings: ≥40°C, ≥90% humidity, ≥20 mm rain in one hour.')
    if warnings.empty: st.info('No threshold alerts recorded.')
    else: st.dataframe(warnings,use_container_width=True)
with tabs[3]:
    st.subheader('Source coverage'); st.dataframe(counts,use_container_width=True)
    st.subheader('Run audit and quality'); st.dataframe(runs,use_container_width=True)
    if not runs.empty:
        st.plotly_chart(px.bar(runs,x='id',y=['received','inserted','rejected'],barmode='group',title='Run-level quality metrics'),use_container_width=True)
with tabs[4]:
    for f in sorted((ROOT/'reports').glob('*')):
        if f.is_file() and f.suffix in ('.csv','.md'):
            st.download_button(f'Download {f.name}',f.read_bytes(),file_name=f.name,key=f.name)
