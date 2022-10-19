"""Download GHCND data for all stations listed in psco_station_ids.py, and save to the station_data directory"""
import requests
from psco_station_ids import psco_station_ids

BASE_URL = "https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access"

for station_id in psco_station_ids:
    csv_name = f"{station_id}.csv"
    station_url = f"{BASE_URL}/{csv_name}"
    print(f"Downloading {csv_name}...")
    resp = requests.get(url=station_url, timeout=120)
    with open(f"station_data/{csv_name}", "w", encoding="utf-8") as f:
        f.write(resp.text)

print("Done")
