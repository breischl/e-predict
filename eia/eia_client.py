"""A dead-simple wrapper around the one EIA OpenData endpoint we use"""
import datetime
import os
from dataclasses import dataclass
from datetime import date

import requests


@dataclass
class DailyDemand:
    """A single day of demand """
    date: date
    """"""
    hour: int
    """Hour of day for data in question"""
    demand: int
    """Electric demand in megawatt-hours"""


def get_electric_demand_hourly(start: date, end: date, respondent: str = "PSCO") -> list[DailyDemand]:
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
    data = json["response"]["data"]

    demand_days: list[DailyDemand] = list()
    for row in data:
        dt = datetime.datetime.strptime(row["period"], "%Y-%m-%dT%H")
        demand_days.append(DailyDemand(date=dt.date(), hour=dt.hour, demand=row["value"]))

    return demand_days
