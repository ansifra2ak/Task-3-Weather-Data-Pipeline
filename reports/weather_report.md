# Weather Data Pipeline Report
Generated UTC: 2026-11-24T08:20:05+00:00
Live pipeline: success; database integrity: ok
Historical results are ERA5 reanalysis, not station readings. Last 30 days uses the actual calendar window; missing dates are not filled. A separate latest-available 30-day series ends at the newest archive date. All local hours use IST (UTC+05:30).
Extreme hour: temperature >=40°C or <=5°C or rain >=20 mm; compare percentage rather than raw counts. Correlation is Pearson and does not imply causation. Hour buckets are IST hours containing UTC-hour samples.

## City Averages
```
              city  avg_temp_c  records
           Chennai       28.66     8760
             Surat       27.75     8760
            Mumbai       27.69     8760
         Ahmedabad       27.54     8760
Thiruvananthapuram       27.47     8760
     Visakhapatnam       27.41     8760
             Kochi       27.38     8760
            Nagpur       27.30     8760
         Hyderabad       26.46     8760
           Kolkata       26.26     8760
              Pune       25.54     8760
           Lucknow       25.36     8760
            Jaipur       25.04     8760
             Delhi       24.85     8760
         Bengaluru       23.94     8760
```
Full data: city_averages.csv

## Last 30 Days
```
       day               city  avg_temp_c  hours
2026-10-26          Hyderabad       25.75     24
2026-10-26              Kochi       27.45     24
2026-10-26             Mumbai       29.64     24
2026-10-26              Delhi       23.36     24
2026-10-26          Bengaluru       22.60     24
2026-10-26            Chennai       28.15     24
2026-10-26            Kolkata       27.70     24
2026-10-26               Pune       26.08     24
2026-10-26          Ahmedabad       26.46     24
2026-10-26             Jaipur       25.08     24
2026-10-26            Lucknow       24.95     24
2026-10-26              Surat       30.08     24
2026-10-26      Visakhapatnam       28.07     24
2026-10-26 Thiruvananthapuram       27.57     24
2026-10-26             Nagpur       25.82     24
2026-10-27          Hyderabad       25.94     24
2026-10-27              Kochi       28.18     24
2026-10-27             Mumbai       28.60     24
2026-10-27              Delhi       22.89     24
2026-10-27          Bengaluru       22.03     24
```
Full data: last_30_days.csv

## Latest Available 30 Days
```
       day               city  avg_temp_c  hours
2026-10-21          Hyderabad       26.94     24
2026-10-21              Kochi       26.92     24
2026-10-21             Mumbai       30.20     24
2026-10-21              Delhi       24.70     24
2026-10-21          Bengaluru       23.63     24
2026-10-21            Chennai       27.34     24
2026-10-21            Kolkata       27.25     24
2026-10-21               Pune       27.18     24
2026-10-21          Ahmedabad       27.83     24
2026-10-21             Jaipur       25.55     24
2026-10-21            Lucknow       24.13     24
2026-10-21              Surat       31.04     24
2026-10-21      Visakhapatnam       28.57     24
2026-10-21 Thiruvananthapuram       27.23     24
2026-10-21             Nagpur       27.02     24
2026-10-22          Hyderabad       27.34     24
2026-10-22              Kochi       25.96     24
2026-10-22             Mumbai       30.23     24
2026-10-22              Delhi       24.89     24
2026-10-22          Bengaluru       23.54     24
```
Full data: latest_available_30_days.csv

## Humidity Rain Correlation
```
              city  pearson_r  paired_hours
         Ahmedabad   0.231072          8760
         Bengaluru   0.123943          8760
           Chennai   0.222068          8760
             Delhi   0.112108          8760
         Hyderabad   0.194538          8760
            Jaipur   0.192008          8760
             Kochi   0.169355          8760
           Kolkata   0.129287          8760
           Lucknow   0.176710          8760
            Mumbai   0.211582          8760
            Nagpur   0.268785          8760
              Pune   0.246326          8760
             Surat   0.239873          8760
Thiruvananthapuram   0.149548          8760
     Visakhapatnam   0.187813          8760
```
Full data: humidity_rain_correlation.csv

## Seasonal Extremes
```
      season  hours  extreme_hours  extreme_pct  max_temp_c  max_rain_mm
 Pre-monsoon  33120            823         2.48        45.4         15.7
     Monsoon  43920            126         0.29        43.3         30.6
      Winter  32400              3         0.01        34.6         10.0
Post-monsoon  21960              1         0.00        37.2         22.2
```
Full data: seasonal_extremes.csv

## Peak Hours Ist
```
              city local_hour  avg_temp_c  samples
         Ahmedabad         14       33.17      365
         Bengaluru         14       28.76      365
           Chennai         13       31.30      365
             Delhi         14       30.56      365
         Hyderabad         14       31.64      365
            Jaipur         14       30.84      365
             Kochi         14       31.39      365
           Kolkata         13       30.67      365
           Lucknow         14       31.06      365
            Mumbai         14       31.12      365
            Nagpur         14       33.25      365
              Pune         14       30.89      365
             Surat         14       30.53      365
Thiruvananthapuram         14       29.74      365
     Visakhapatnam         13       30.27      365
```
Full data: peak_hours_IST.csv

## Latest Weather
```
              city               observed_at  temperature_c  humidity  pressure_hpa  wind_mps  rain_mm     condition
         Ahmedabad 2026-11-24T08:13:50+00:00          29.99      25.0        1017.0      3.09     0.00     clear sky
         Bengaluru 2026-11-24T08:16:57+00:00          27.11      65.0        1014.0      3.09     1.01 moderate rain
           Chennai 2026-11-24T08:10:09+00:00          29.01      82.0        1013.0      6.17     0.00          mist
             Delhi 2026-11-24T08:15:22+00:00          24.99      47.0        1019.0      4.63     0.00          haze
         Hyderabad 2026-11-24T08:11:44+00:00          30.23      45.0        1018.0      4.12     0.00          haze
            Jaipur 2026-11-24T08:13:28+00:00          25.69      17.0        1020.0      2.57     0.00          haze
             Kochi 2026-11-24T08:17:59+00:00          33.99      54.0        1011.0      3.68     0.00 broken clouds
           Kolkata 2026-11-24T08:12:13+00:00          27.96      54.0        1016.0      3.60     0.00          haze
           Lucknow 2026-11-24T08:11:45+00:00          26.05      44.0        1018.0      0.00     0.00          haze
            Mumbai 2026-11-24T08:16:55+00:00          34.03      33.0        1014.0      3.60     0.00         smoke
            Nagpur 2026-11-24T08:10:41+00:00          29.00      42.0        1018.0      2.06     0.00          haze
              Pune 2026-11-24T08:15:55+00:00          30.74      15.0        1015.0      2.79     0.00     clear sky
             Surat 2026-11-24T08:11:46+00:00          32.94      31.0        1016.0      2.57     0.00         smoke
Thiruvananthapuram 2026-11-24T08:19:02+00:00          30.85      70.0        1011.0      4.12     0.00          haze
     Visakhapatnam 2026-11-24T08:11:46+00:00          28.78      74.0        1014.0      2.57     0.00          haze
```
Full data: latest_weather.csv

## Alerts
No data available.
Full data: alerts.csv

## Coverage
```
        source  records  cities              first_record               last_record
OpenWeatherMap       87      15 2026-11-24T07:08:18+00:00 2026-11-24T08:19:02+00:00
    Open-Meteo   131400      15 2025-11-19T00:00:00+00:00 2026-11-18T23:00:00+00:00
```
Full data: coverage.csv

## Pipeline Runs
```
 id  source_id                   started                  finished  status  expected  received  inserted  rejected error         source
 26          1 2026-11-24T08:20:03+00:00 2026-11-24T08:20:05+00:00 success        15        15         0         0       OpenWeatherMap
 25          1 2026-11-24T08:19:01+00:00 2026-11-24T08:19:02+00:00 success        15        15         1         0       OpenWeatherMap
 24          1 2026-11-24T08:17:58+00:00 2026-11-24T08:18:00+00:00 success        15        15         1         0       OpenWeatherMap
 23          1 2026-11-24T08:16:56+00:00 2026-11-24T08:16:58+00:00 success        15        15         3         0       OpenWeatherMap
 22          1 2026-11-24T08:15:54+00:00 2026-11-24T08:15:56+00:00 success        15        15         1         0       OpenWeatherMap
 21          1 2026-11-24T08:14:51+00:00 2026-11-24T08:14:54+00:00 success        15        15         0         0       OpenWeatherMap
 20          1 2026-11-24T08:13:49+00:00 2026-11-24T08:13:50+00:00 success        15        15         3         0       OpenWeatherMap
 19          1 2026-11-24T08:12:46+00:00 2026-11-24T08:12:48+00:00 success        15        15         0         0       OpenWeatherMap
 18          1 2026-11-24T08:11:42+00:00 2026-11-24T08:11:46+00:00 success        15        15         5         0       OpenWeatherMap
 17          1 2026-11-24T08:10:40+00:00 2026-11-24T08:10:41+00:00 success        15        15         1         0       OpenWeatherMap
 16          1 2026-11-24T08:09:37+00:00 2026-11-24T08:09:39+00:00 success        15        15         0         0       OpenWeatherMap
 15          1 2026-11-24T08:08:35+00:00 2026-11-24T08:08:37+00:00 success        15        15         1         0       OpenWeatherMap
 14          1 2026-11-24T08:07:33+00:00 2026-11-24T08:07:35+00:00 success        15        15         2         0       OpenWeatherMap
 13          1 2026-11-24T08:06:31+00:00 2026-11-24T08:06:33+00:00 success        15        15         2         0       OpenWeatherMap
 12          1 2026-11-24T08:05:29+00:00 2026-11-24T08:05:30+00:00 success        15        15         1         0       OpenWeatherMap
 11          1 2026-11-24T08:04:27+00:00 2026-11-24T08:04:28+00:00 success        15        15         0         0       OpenWeatherMap
 10          1 2026-11-24T08:03:24+00:00 2026-11-24T08:03:26+00:00 success        15        15         3         0       OpenWeatherMap
  9          1 2026-11-24T08:02:22+00:00 2026-11-24T08:02:24+00:00 success        15        15         0         0       OpenWeatherMap
  8          1 2026-11-24T08:01:20+00:00 2026-11-24T08:01:22+00:00 success        15        15        15         0       OpenWeatherMap
  7          1 2026-11-24T07:47:12+00:00 2026-11-24T07:47:16+00:00 success        15        15        15         0       OpenWeatherMap
```
Full data: pipeline_runs.csv
