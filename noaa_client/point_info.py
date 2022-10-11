from dataclasses import dataclass


@dataclass
class PointInfo:
    """Information returned from the NOAA /points API endpoint"""
    id: str
    latitude: float
    longitude: float
    gridId: str
    gridX: int
    gridY: int
