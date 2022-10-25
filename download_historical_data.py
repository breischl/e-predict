import os
from datetime import date

import dotenv
import numpy as np
import pandas as pd
import requests
from json_encoder import json

import eia.eia_client as eia
import ghcnd.station_observations


def download_eia_historical_data(electric_data_dir: str, eia_respondent: str = "PSCO"):
    """Download historical usage data from the EIA"""
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


def cleanse_eia_data(electric_data_dir: str, eia_respondent: str = "PSCO"):
    """Clean up already-downloaded EIA data and save daily & hourly dataframe files"""
    print("Cleansing EIA data")
    eia_file = os.path.join(electric_data_dir, f"{eia_respondent}.json")
    df: pd.DataFrame = pd.read_json(eia_file, typ="frame", orient="records", convert_dates=["dates"])
    df.set_index("date", inplace=True)

    # print(demand_ds.describe())
    # demand_ds.plot.hist()
    # demand_ds.plot()

    # calculate inter-quartile range
    iqr = df.quantile(0.75, numeric_only=False) - df.quantile(0.25, numeric_only=False)

    # Find values within `iqr_mult` multiples of the median
    iqr_mult = 3
    median = df.median()
    min_demand = median - (iqr * iqr_mult)
    max_demand = median + (iqr * iqr_mult)
    print(f"inter-quartile range: {iqr['demand']}, median: {median['demand']}, valid data range: {min_demand['demand']} - {max_demand['demand']}")

    valid_rows = np.abs((df - median) / iqr) < iqr_mult

    # replace outliers with nan, then interpolate those values
    df = df.where(valid_rows, np.nan)
    df.interpolate(inplace=True)

    # Save the cleaned hourly dataframe
    df_file_path = os.path.join(electric_data_dir, "psco-hourly-dataframe.json")
    df.to_json(df_file_path)

    # Group and sum into daily totals
    grouped = df.groupby(lambda x: x.date, sort=False).agg(
        daily_demand=("demand", np.sum),
        num_hours_reported=("demand", np.count_nonzero)
    )

    # Drop days with less than 24 hours of data (usually first & last day of range)
    grouped = grouped[grouped.num_hours_reported == 24].drop(labels="num_hours_reported", axis=1)

    grouped_file_path = os.path.join(electric_data_dir, "psco-daily-dataframe.json")
    grouped.to_json(grouped_file_path)


def download_ghcnd_historical_data(weather_data_dir: str, weather_station_ids: list[str]):
    """Download and cleanse historical weather data from GHCND"""
    ghcnd_base_url = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all"

    print("Downloading historical weather data from GHCN-d...")

    if not os.path.exists(weather_data_dir):
        os.makedirs(weather_data_dir)

    for station_id in weather_station_ids:
        dly_name = f"{station_id}.dly"
        dly_file_path = os.path.join(weather_data_dir, dly_name)
        station_url = f"{ghcnd_base_url}/{dly_name}"

        print(f"Downloading {station_url} to {dly_file_path}...")

        resp = requests.get(url=station_url, timeout=120)
        with open(dly_file_path, "w", encoding="utf-8") as f:
            f.write(resp.text)

        # Cleanse data and write out DataFrame
        obs = ghcnd.station_observations.parse_from_dly_text(resp.text)

        hist_temp_df = pd.DataFrame(obs.observations)

        # hist_temp_df["date"] = pd.to_datetime(hist_temp_df["date"])
        # hist_temp_df = hist_temp_df.assign(day_of_year=lambda x: x["date"].dt.day_of_year)

        hist_temp_df.set_index("date", inplace=True)

        hist_temp_df = hist_temp_df.interpolate(method="time")

        hist_temp_df = hist_temp_df.assign(
            tmax_decimal=lambda x: x["tmax"] / 10.0,
            tmin_decimal=lambda x: x["tmin"] / 10.0)

        df_file_path = os.path.join(weather_data_dir, f"{station_id}-dataframe.json")
        hist_temp_df.to_json(df_file_path)

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

    dotenv.load_dotenv()

    download_eia_historical_data(ELECTRIC_DATA_DIR, eia_respondent="PSCO")
    cleanse_eia_data(ELECTRIC_DATA_DIR, eia_respondent="PSCO")
    download_ghcnd_historical_data(WEATHER_DATA_DIR, WEATHER_STATION_IDS)
