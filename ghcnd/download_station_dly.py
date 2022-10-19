"""Download GHCND data for all stations listed in psco_station_ids.py, and save to the station_data directory"""
import requests
from psco_station_ids import psco_station_ids

BASE_URL = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all"

for station_id in psco_station_ids:
    dly_name = f"{station_id}.dly"
    station_url = f"{BASE_URL}/{dly_name}"
    print(f"Downloading {station_url}...")
    resp = requests.get(url=station_url, timeout=120)
    with open(f"station_data/{dly_name}", "w", encoding="utf-8") as f:
        f.write(resp.text)

print("Done")
