from dataclasses import dataclass
from datetime import datetime

from noaa_client.noaa_metadata import NoaaMetadata

# pylint: disable=missing-function-docstring


@dataclass
class ForecastPeriod:
    """A single period in a NOAA forecast"""
    json: dict
    """JSON for this period from the NOAA response"""

    @property
    def number(self) -> int:
        """A 1-indexed sequence number for this forecast period in the context of the overall forecast"""
        return self.json["number"]

    @property
    def name(self) -> str:
        return self.json["name"]

    @property
    def is_day_time(self) -> bool:
        return self.json["isDaytime"]

    @property
    def start_time(self) -> datetime:
        return datetime.fromisoformat(self.json["startTime"])

    @property
    def end_time(self) -> datetime:
        return datetime.fromisoformat(self.json["endTime"])

    @property
    def temperature(self) -> float:
        return self.json["temperature"]

    @property
    def temperature_unit(self) -> str:
        return self.json["temperatureUnit"]


@dataclass
class PointForecast:
    """A forecast for a single 'point' (really 2.5km square)"""

    json: dict
    """JSON from the NOAA response"""
    meta: NoaaMetadata
    """Response metadata from NOAA"""

    @ property
    def periods(self) -> list[ForecastPeriod]:
        """The set of forecast periods"""
        return [ForecastPeriod(fp) for fp in self.json["properties"]["periods"]]

    @ property
    def updated(self) -> datetime:
        return datetime.fromisoformat(self.json["properties"]["updated"])

    @ property
    def valid_times(self) -> str:
        return self.json["properties"]["validTimes"]
