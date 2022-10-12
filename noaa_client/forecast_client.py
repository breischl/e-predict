import requests

from noaa_client.noaa_metadata import parse as parse_metadata
from noaa_client.point_info import PointInfo
from noaa_client.point_info import parse as parse_point_info


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
        url = f"{self.base_url}/points/{latitude},{longitude}"
        resp = requests.get(url, headers=self.headers, timeout=120)
        resp.raise_for_status()

        meta = parse_metadata(resp.headers)
        json = resp.json()
        return parse_point_info(json, meta)
