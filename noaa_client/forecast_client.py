from urllib.parse import quote

import requests

from noaa_client.point_info import PointInfo


class ForecastClient:
    """Wrapper for the NOAA Forecast weather API.

    Wraps calls to the NOAA Forecast API at https://www.weather.gov/documentation/services-web-api
    """

    def __init__(self, user_agent: str, base_url="https://api.weather.gov") -> None:
        """Create a new ForecastClient.

        Args:
            user_agent:
                user_agent header value sent with requests to NOAA.
                Should include app name and admin email.
                eg (my-app, some-admin@example.com)

        Raises:
            ValueError: user_agent was not provided or was falsey
        """
        if not user_agent:
            raise ValueError("user_agent")

        self.base_url = base_url
        self.headers = {
            "User-Agent": user_agent,
            "Accept": "application/geo+json"
        }

    def points(self, latitude: any, longitude: any) -> PointInfo:
        """Get information about a particular map/geo point from NOAA

        Args:
            latitude: Latitude given as either a float or a string
            longitude: Longitude gives as either a float or a string
        """
        quoted_lat_long = quote(f"{latitude},{longitude}")
        url = f"{self.base_url}/points/{quoted_lat_long}"
        resp = requests.get(url, headers=self.headers, timeout=120)
        resp.raise_for_status()

        json = resp.json()
        props = json["properties"]
        coords = props["relativeLocation"]["geometry"]["coordinates"]
        return PointInfo(id=props["@id"],
                         latitude=coords[1],
                         longitude=coords[0],
                         grid_id=props["gridId"],
                         grid_x=props["gridX"],
                         grid_y=props["gridY"]
                         )
