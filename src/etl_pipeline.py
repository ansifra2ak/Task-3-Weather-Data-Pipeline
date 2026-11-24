"""Extract, validate, transactionally load, and record audit metrics."""
import logging
from datetime import datetime, timezone, timedelta
from config.settings import ROOT, CITIES, DB, HISTORY_DAYS, ARCHIVE_LAG_DAYS
from src import database as db, api_client as api
from src.validators import validate

logger=logging.getLogger('weather')

def configure_logging():
    from logging.handlers import RotatingFileHandler
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler=RotatingFileHandler(ROOT/'logs/pipeline.log',maxBytes=1_000_000,backupCount=2)
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
        logger.addHandler(handler)
        logger.addHandler(logging.StreamHandler())

def run(source, path=DB, cities=CITIES, extractor=None, start=None, end=None):
    configure_logging(); db.setup(path)
    historical=source=='Open-Meteo'
    end=end or datetime.now(timezone.utc).date()-timedelta(days=ARCHIVE_LAG_DAYS)
    start=start or end-timedelta(days=HISTORY_DAYS-1)
    expected=len(cities)*((end-start).days+1)*24 if historical else len(cities)
    run_id=db.start_run(source,expected,path)
    received=inserted=rejected=success=0; errors=[]
    for city in cities:
        try:
            raw=extractor(city) if extractor else (api.archive(city,start,end) if historical else [api.live(city,api.api_key())])
            received+=len(raw); clean=[]
            for row in raw:
                try: clean.append(validate(row))
                except (TypeError,ValueError,OverflowError): rejected+=1
            inserted+=db.store(city[0],source,clean,path)
            if clean: success+=1
            else: errors.append(f'{city[0]}: no valid records')
            logger.info('%s %s: %s valid rows',source,city[0],len(clean))
        except Exception as exc:
            # Do not log raw requests, which may contain credentials.
            msg=f'{city[0]}: {exc if isinstance(exc,RuntimeError) and str(exc).startswith(('HTTP ','Weather provider','Incomplete archive')) else type(exc).__name__}'
            errors.append(msg); logger.error('%s',msg)
    status='success' if success==len(cities) and not rejected and received>=expected else ('partial' if success else 'failed')
    db.finish_run(run_id,status,received,inserted,rejected,'; '.join(errors),path)
    logger.info('Run %s %s: received=%s inserted=%s rejected=%s',run_id,status,received,inserted,rejected)
    return {'status':status,'received':received,'inserted':inserted,'rejected':rejected,'errors':errors}
