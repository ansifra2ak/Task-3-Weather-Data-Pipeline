from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / 'database/weather_data.db'
CITIES = [
 ('Hyderabad',17.385,78.487), ('Kochi',9.931,76.267), ('Mumbai',19.076,72.878),
 ('Delhi',28.614,77.209), ('Bengaluru',12.972,77.595), ('Chennai',13.083,80.271),
 ('Kolkata',22.573,88.364), ('Pune',18.520,73.857), ('Ahmedabad',23.023,72.571),
 ('Jaipur',26.912,75.787), ('Lucknow',26.847,80.946), ('Surat',21.170,72.831),
 ('Visakhapatnam',17.687,83.218), ('Thiruvananthapuram',8.524,76.937), ('Nagpur',21.146,79.088)]
INTERVAL_MINUTES = 60
HISTORY_DAYS = 365
ARCHIVE_LAG_DAYS = 6
THRESHOLDS = {'temperature_c': 40, 'humidity': 90, 'rain_mm': 20}