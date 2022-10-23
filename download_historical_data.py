import os
from datetime import date

import dotenv
import requests
from json_encoder import json

import eia.eia_client as eia


def download_historical_data(electric_data_dir: str, weather_data_dir: str, weather_station_ids: list[str], eia_respondent: str = "PSCO"):

    GHCND_BASE_URL = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all"

    dotenv.load_dotenv()

    ###################################
    # Download EIA electric usage data
    ###################################
    start_date = date(2015, 1, 1)
    end_date = date.today()

    print("Downloading EIA demand data...")
    usage_data = eia.get_electric_demand_hourly(start_date, end_date, respondent=eia_respondent)

    if not os.path.exists(electric_data_dir):
        os.makedirs(electric_data_dir)

    eia_file = os.path.join(electric_data_dir, f"{eia_respondent}.json")
    print(f"Writing EIA demand data to {eia_file}...")
    with open(eia_file, "w", encoding="utf-8") as f:
        json.dump(usage_data, f, indent=4, allow_nan=True)

    print("Completed downloading EIA demand data")

    #########################
    # Download GHCN-d Weather Data
    #########################

    print("Downloading historical weather data from GHCN-d...")

    if not os.path.exists(weather_data_dir):
        os.makedirs(weather_data_dir)

    for station_id in weather_station_ids:
        dly_name = f"{station_id}.dly"
        dly_file_path = os.path.join(weather_data_dir, dly_name)
        station_url = f"{GHCND_BASE_URL}/{dly_name}"

        print(f"Downloading {station_url} to {dly_file_path}...")

        resp = requests.get(url=station_url, timeout=120)
        with open(dly_file_path, "w", encoding="utf-8") as f:
            f.write(resp.text)

    print("Finished downloading data")


if __name__ == "__main__":
    HISTORICAL_DATA_DIR = os.path.abspath("./historical_data")
    ELECTRIC_DATA_DIR = os.path.join(HISTORICAL_DATA_DIR, "electric_data")
    WEATHER_DATA_DIR = os.path.join(HISTORICAL_DATA_DIR, "weather_station_data")
    WEATHER_STATION_IDS = [
        "USW00023066",  # Grand Junction Walker Field
        "USC00053553",  # Greeley UNC
        "USC00053005",  # Ft Collins
        "USC00050848",  # Boulder
        "USC00055984",  # Northglenn
        "USC00058995",  # Wheat Ridge
        "USW00023061"  # Alamosa
    ]

    download_historical_data(ELECTRIC_DATA_DIR, WEATHER_DATA_DIR, WEATHER_STATION_IDS, eia_respondent="PSCO")
