from dataclasses import dataclass


@dataclass
class PointInfo:
    """Information returned from the NOAA /points API endpoint"""
    id: str  # pylint: disable=invalid-name
    latitude: float
    longitude: float
    grid_id: str
    grid_x: int
    grid_y: int
