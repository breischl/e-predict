import calendar
from dataclasses import dataclass
from datetime import date
from math import nan as NaN
from typing import Tuple


@dataclass
class StationDayObservations:
    """A single day worth of weather observations for a single GHCN-d station"""
    date: date
    tmax: int
    """Max temperature in tenths-of-a-degree C"""
    tmin: int
    """Min temperature in tenths-of-a-degree C"""

    @property
    def tmax_decimal(self) -> float:
        """tmin converted to decimal degrees (ie, the normal way you see temps represented)"""
        return self.tmax / 10.0

    @property
    def tmin_decimal(self) -> float:
        """tmin converted to decimal degrees (ie, the normal way you see temps represented)"""
        return self.tmin / 10.0

    @property
    def is_empty(self) -> bool:
        """Indicates if all observation values for this day are None/NaN"""
        return (self.tmax is NaN and self.tmin is NaN)


@dataclass
class StationObservations:
    """A set of observations for a station"""
    station_id: str
    """Station ID"""
    observations: list[StationDayObservations]

    @property
    def start_date(self) -> date:
        """First date of observations"""
        return self.observations[0].date

    @property
    def end_date(self) -> date:
        """Last date of observations"""
        return self.observations[-1].date


DEFAULT_MEASUREMENTS: set[str] = frozenset(["TMAX", "TMIN"])
DEFAULT_START_DATE: date = date(2015, 1, 1)


def read_from_dly_file(dly_file_path: str, desired_measurements: set[str] = DEFAULT_MEASUREMENTS, start_date: date = DEFAULT_START_DATE) -> StationObservations:
    """Parse StationObservations from a .dly text file"""
    with open(dly_file_path, "r", encoding="utf-8") as f:
        return parse_from_dly_text(f.read(), desired_measurements, start_date)


def parse_from_dly_text(dly_text: str, desired_measurements: set[str] = DEFAULT_MEASUREMENTS, start_date: date = DEFAULT_START_DATE) -> StationObservations:
    """Parse StationObservations from a .dly text string

    The returned observations will be sorted in date order. Days with no valid observations will be trimmed from the end only.
    There may still be days with no observations in the middle of the date range, as long as there is at least one valid day afterwards.
    """
    observations: dict[date, StationDayObservations] = {}

    station_id: str = None

    for line in dly_text.splitlines():
        if not station_id:
            station_id = line[0:11]

        (year, month, elem, day_observations_values) = _parse_from_dly_line(line, desired_measurements)
        if elem not in desired_measurements:
            continue

        for (day_ord, observation_value) in enumerate(day_observations_values):
            dt = date(year, month, day_ord + 1)
            if dt < start_date:
                continue

            day_obs = observations.get(dt, StationDayObservations(dt, None, None))

            if elem == "TMAX":
                day_obs.tmax = observation_value
            elif elem == "TMIN":
                day_obs.tmin = observation_value

            observations[day_obs.date] = day_obs

    sorted_obs = sorted(observations.values(), key=lambda obs: obs.date)

    # Strip fully-empty observations from the end of the list.
    # This almost always happens because each line is a full month of data, but we're almost always retrieving it
    # partway through the month, so the remaining days in the current month are null
    while sorted_obs[-1].is_empty:
        sorted_obs.pop()

    return StationObservations(station_id, sorted_obs)


def _parse_from_dly_line(dly_line: str, desired_measures: set[str]) -> Tuple[int, int, str, list[int]]:
    """Parse a month of StationDayObervations from a line in a GHCN .dly file

    Each line contains a month of data, hence this method returns a list, with one object for each day.
    Currently we only parse out the temperature min/max

    The format for the .dly files can be found in: https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt
    Copying from there:
    Each record in a file contains one month of daily data.  The variables on each line include the following:\
    ------------------------------
    Variable   Columns   Type
    ------------------------------
    ID            1-11   Character
    YEAR         12-15   Integer
    MONTH        16-17   Integer
    ELEMENT      18-21   Character
    VALUE1       22-26   Integer
    MFLAG1       27-27   Character
    QFLAG1       28-28   Character
    SFLAG1       29-29   Character
    VALUE2       30-34   Integer
    MFLAG2       35-35   Character
    QFLAG2       36-36   Character
    SFLAG2       37-37   Character
    .           .          .
    .           .          .
    .           .          .
    VALUE31    262-266   Integer
    MFLAG31    267-267   Character
    QFLAG31    268-268   Character
    SFLAG31    269-269   Character
    ------------------------------
    """

    element = dly_line[17:21]
    if element not in desired_measures:
        # We don't care about this measurement
        return (None, None, element, None)

    year = int(dly_line[11:15])
    month = int(dly_line[15:17])

    (_, last_day_of_month) = calendar.monthrange(year, month)

    measurements: list[int] = list()
    for day_idx in range(0, last_day_of_month):
        start_idx = (day_idx * 8) + 21

        # Extract measurement, note we're skipping the flags
        raw_measurement = dly_line[start_idx:start_idx + 5]
        parsed_measure = int(raw_measurement)
        if parsed_measure == -9999:  # Special value indicating missing data
            parsed_measure = NaN
        measurements.append(parsed_measure)

    return (year, month, element, measurements)
