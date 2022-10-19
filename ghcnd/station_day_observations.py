from dataclasses import dataclass
import calendar
from datetime import date, datetime
from typing import Tuple


@dataclass
class StationDayObservations:
    """A single day worth of weather observations for a single GHCN-d station"""
    date: date
    temp_max: int
    """Max temperature in tenths-of-a-degree C"""
    temp_min: int
    """Min temperature in tenths-of-a-degree C"""


def parse_from_dly_text(dly_text: str) -> list[StationDayObservations]:
    """Parse observation from a .dly text file"""
    observations: list[StationDayObservations] = list()
    obs_year = 0
    obs_month = 0
    month_observations = {}
    for line in dly_text.splitlines():
        # TODO: We're wasting effort parsing out observations that we'll just throw away
        (new_year, new_month, elem, day_observations) = parse_from_dly_line(line)
        if new_year != obs_year or new_month != obs_month:
            if month_observations:
                for (day_ord, (tmax, tmin)) in enumerate(zip(month_observations["TMAX"], month_observations["TMIN"])):
                    day = date(obs_year, obs_month, day_ord + 1)
                    day_obs = StationDayObservations(day, tmax, tmin)
                    observations.append(day_obs)
            month_observations.clear()
            obs_year = new_year
            obs_month = new_month

        month_observations[elem] = day_observations
    month_observations[elem] = day_observations

    return observations


def parse_from_dly_line(dly_line: str) -> Tuple[int, int, str, list[int]]:
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

    year = int(dly_line[11:15])
    month = int(dly_line[15:17])
    (_, last_day_of_month) = calendar.monthrange(year, month)
    element = dly_line[17:21]
    measurements: list[int] = list()
    for day_idx in range(0, last_day_of_month):
        start_idx = (day_idx * 8) + 22

        # Extract measurement, note we're skipping the flags
        raw_measurement = dly_line[start_idx:start_idx + 4]
        parsed_measure = int(raw_measurement)
        if parsed_measure == -9999:  # Special value indicating missing data
            parsed_measure = None
        measurements.append(parsed_measure)

    return (year, month, element, measurements)
