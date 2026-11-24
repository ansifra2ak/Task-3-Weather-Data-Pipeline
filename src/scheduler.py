"""Collect at fixed intervals while the local process is running."""
import time
from datetime import date
from config.settings import INTERVAL_MINUTES
from src.etl_pipeline import run, configure_logging, logger
from src.reporter import generate
from src.database import backup

def serve():
    configure_logging()
    last_backup=None
    while True:
        time.sleep(INTERVAL_MINUTES*60)
        try:
            run('OpenWeatherMap')
            generate()
            if last_backup!=date.today():
                backup()
                last_backup=date.today()
        except Exception as exc:
            logger.error('Scheduled cycle failed: %s',type(exc).__name__)
