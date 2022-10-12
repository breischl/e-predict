from dataclasses import dataclass

from noaa_client.noaa_metadata import NoaaMetadata


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
    metadata: NoaaMetadata


def parse(json: dict, meta: NoaaMetadata) -> PointInfo:
    props = json["properties"]
    coords = props["relativeLocation"]["geometry"]["coordinates"]

    return PointInfo(id=props["@id"],
                     latitude=coords[1],
                     longitude=coords[0],
                     grid_id=props["gridId"],
                     grid_x=props["gridX"],
                     grid_y=props["gridY"],
                     metadata=meta
                     )
