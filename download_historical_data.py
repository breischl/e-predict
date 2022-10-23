import os
from datetime import date

import dotenv
import requests
from json_encoder import json

import eia.eia_client as eia


def download_historical_data():
    ###################################
    # Configs
    ###################################
    DATA_DIR = "historical_data"

    PSCO_STATION_IDS = [
        "USW00023066",  # Grand Junction Walker Field
        "USC00053553",  # Greeley UNC
        "USC00053005",  # Ft Collins
        "USC00050848",  # Boulder
        "USC00055984",  # Northglenn
        "USC00058995",  # Wheat Ridge
        "USW00023061"  # Alamosa
    ]

    GHCND_BASE_URL = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all"

    EIA_RESPONDENT = "PSCO"

    dotenv.load_dotenv()

    ###################################
    # Download EIA electric usage data
    ###################################
    print(f"Downloading historical data to {DATA_DIR}")

    start_date = date(2015, 1, 1)
    end_date = date.today()

    print("Downloading EIA demand data...")
    usage_data = eia.get_electric_demand_hourly(start_date, end_date, respondent=EIA_RESPONDENT)

    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)

    EIA_FILE = os.path.join(DATA_DIR, "electric_data", f"{EIA_RESPONDENT}.json")
    print(f"Writing EIA demand data to {EIA_FILE}...")
    with open(EIA_FILE, "w", encoding="utf-8") as f:
        json.dump(usage_data, f, indent=4, allow_nan=True)

    print("Completed downloading EIA demand data")

    #########################
    # Download GHCN-d Weather Data
    #########################

    DLY_FILE_DIR = os.path.join(DATA_DIR, "weather_station_data")
    if not os.path.exists(DLY_FILE_DIR):
        os.mkdir(DLY_FILE_DIR)

    for station_id in PSCO_STATION_IDS:
        dly_name = f"{station_id}.dly"
        dly_file_path = os.path.join(DLY_FILE_DIR, dly_name)
        station_url = f"{GHCND_BASE_URL}/{dly_name}"

        print(f"Downloading {station_url} to {dly_file_path}...")

        resp = requests.get(url=station_url, timeout=120)
        with open(dly_file_path, "w", encoding="utf-8") as f:
            f.write(resp.text)


if __name__ == "main":
    download_historical_data()
