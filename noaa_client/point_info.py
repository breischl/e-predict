from dataclasses import dataclass


@dataclass
class PointInfo:
    """Information returned from the NOAA /points API endpoint

    Currently this is just a subset of the available information. See
    https://www.weather.gov/documentation/services-web-api#/default/point for more
    """
    id: str  # pylint: disable=invalid-name
    latitude: float
    longitude: float
    grid_id: str
    grid_x: int
    grid_y: int
