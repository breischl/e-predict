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


def get_electric_demand_hourly(start: date, end: date, respondent: str = "PSCO") -> list[HourlyDemand]:
    """Get hourly electric demand for a particular date range and respondent

    Based on the EIA OpenData https://api.eia.gov/v2/electricity/rto/region-data/data endpoint"""

    api_key = os.environ.get("EIA_TOKEN")

    URL = "https://api.eia.gov/v2/electricity/rto/region-data/data"
    params = {
        "data[]": "value",
        "facets[respondent][]": respondent,
        "facets[type][]": "D",
        "frequency": "hourly",  # or "local-hourly"
        "api_key": api_key,
        "start": start,
        "end": end
    }
    resp = requests.get(URL, params, timeout=120)
    json = resp.json()
    resp.raise_for_status()

    data = json["response"]["data"]

    demand_days: list[HourlyDemand] = list()
    for row in data:
        dt = datetime.datetime.strptime(row["period"], "%Y-%m-%dT%H")
        demand_days.append(HourlyDemand(date=dt, demand=row["value"]))

    return demand_days
