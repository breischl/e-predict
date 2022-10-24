"""A dead-simple wrapper around the one EIA OpenData endpoint we use"""
import datetime
import os
from dataclasses import dataclass
from datetime import date

import requests
from json_encoder.json import json_encoder


@dataclass
class HourlyDemand():

    """A single day of demand """
    date: datetime
    """"""
    demand: int
    """Electric demand in megawatt-hours"""

    def to_dict(self) -> dict:
        """Convert object to a dictionary"""
        return {
            "date": self.date.isoformat(),
            "demand": self.demand
        }


@json_encoder.register(HourlyDemand)
def encode_hourlydemand(obj):
    """Encoding function for use with json-encoder library"""
    return obj.to_dict()


def get_electric_demand_hourly(start: date, end: date = None, respondent: str = "PSCO", results_per_request: int = 5000) -> list[HourlyDemand]:
    """Get hourly electric demand for a particular date range and respondent.
    This will automatically perform pagination, so it may execute multiple requests under the covers. 
    Based on the EIA OpenData API. See the /support/Electricity Production.md file for more documentation of the API

    Requires an environment variable "EIA_TOKEN" be set with a valid EIA OpenData API token.

    Args:
        start: earliest date of retrieved data
        end: (optional) latest date of retrieved data. If None, then get all available data after `start` date. 
        respondent: (optional, default "PSCO") the EIA respondent to retrieve data for
        max_results: (optional, default 5000) maximum number of data points to return per request
    """

    api_key = os.environ.get("EIA_TOKEN")
    if not api_key:
        raise ValueError("EIA_TOKEN environment variable not set")

    URL = "https://api.eia.gov/v2/electricity/rto/region-data/data"

    params = {
        "data[]": "value",
        "facets[respondent][]": respondent,
        "facets[type][]": "D",
        "frequency": "hourly",  # or "local-hourly"
        "api_key": api_key,
        "start": start,
        "offset": 0,
        "length": results_per_request
    }

    if end:
        params["end"] = end

    demand_days: list[HourlyDemand] = list()
    expected_result_count = 999_999_999

    while len(demand_days) < expected_result_count:
        print(f"Requesting EIA data from offset {params['offset']}")
        resp = requests.get(URL, params, timeout=120)
        resp.raise_for_status()

        json_resp = resp.json()["response"]

        data = json_resp["data"]
        if not data:
            print("Received no data from EIA, ending iteration")
            break

        for row in data:
            dt = datetime.datetime.strptime(row["period"], "%Y-%m-%dT%H")
            demand_days.append(HourlyDemand(date=dt, demand=row["value"]))

        # Update pagination
        expected_result_count = json_resp["total"]
        params["offset"] = params["offset"] + len(data)

    print(f"Finished requesting EIA data, retrieved {len(demand_days)} data points")

    return demand_days
