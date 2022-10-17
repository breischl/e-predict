from dataclasses import dataclass

from noaa_client.noaa_metadata import NoaaMetadata

# pylint: disable=missing-function-docstring


@dataclass
class PointInfo:
    """Information returned from the NOAA /points API endpoint"""

    json: dict
    metadata: NoaaMetadata

    @property
    def id(self) -> str:
        return self.json["properties"]["@id"]

    @property
    def latitude(self) -> float:
        return self.json["properties"]["relativeLocation"]["geometry"]["coordinates"][1]

    @property
    def longitude(self) -> float:
        return self.json["properties"]["relativeLocation"]["geometry"]["coordinates"][0]

    @property
    def grid_id(self) -> str:
        return self.json["properties"]["gridId"]

    @property
    def grid_x(self) -> int:
        return self.json["properties"]["gridX"]

    @property
    def grid_y(self) -> int:
        return self.json["properties"]["gridY"]
