from typing import Optional
import requests
from noaa_client.point_info import PointInfo
from urllib.parse import quote


class ForecastClient:
    """Wrapper for the NOAA Forecast weather API.

    Wraps calls to the NOAA Forecast API at https://www.weather.gov/documentation/services-web-api
    """

    def __init__(self, user_agent: str, base_url="https://api.weather.gov") -> None:
        """Create a new ForecastClient.

        Args:
            user_agent: user_agent header value sent with requests to NOAA. Should include app name and admin email. eg (my-app, some-admin@example.com)

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

    def points(self, latitude, longitude) -> PointInfo:
        quoted_lat_long = quote(f"{latitude},{longitude}")
        url = f"{self.base_url}/points/{quoted_lat_long}"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()

        json = resp.json()
        props = json["properties"]
        return PointInfo(id=props["@id"],
                         latitude=props["relativeLocation"]["geometry"]["coordinates"][1],
                         longitude=props["relativeLocation"]["geometry"]["coordinates"][0],
                         gridId=props["gridId"],
                         gridX=props["gridX"],
                         gridY=props["gridY"]
                         )
