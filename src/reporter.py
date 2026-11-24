"""Generate real CSV results and a readable report from SQLite."""
from config.settings import ROOT,DB
from src.analytics import results,current,alerts
from src.monitor import health
from src.database import now

def generate(path=DB, folder=ROOT/'reports'):
    folder.mkdir(parents=True,exist_ok=True)
    status,age,counts,runs,integrity=health(path)
    sections=results(path)|{'latest_weather':current(path),'alerts':alerts(path),'coverage':counts,'pipeline_runs':runs}
    lines=['# Weather Data Pipeline Report',f'Generated UTC: {now()}',f'Live pipeline: {status}; database integrity: {integrity}',
           'Historical results are ERA5 reanalysis, not station readings. Last 30 days uses the actual calendar window; missing dates are not filled. A separate latest-available 30-day series ends at the newest archive date. All local hours use IST (UTC+05:30).',
           'Extreme hour: temperature >=40°C or <=5°C or rain >=20 mm; compare percentage rather than raw counts. Correlation is Pearson and does not imply causation. Hour buckets are IST hours containing UTC-hour samples.']
    for name,df in sections.items():
        df.to_csv(folder/f'{name}.csv',index=False)
        lines.extend(['',f'## {name.replace("_"," ").title()}','No data available.' if df.empty else '```\n'+df.head(20).to_string(index=False)+'\n```',f'Full data: {name}.csv'])
    (folder/'weather_report.md').write_text('\n'.join(lines)+'\n')
    return folder/'weather_report.md'
