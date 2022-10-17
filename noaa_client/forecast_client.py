import requests

from noaa_client.noaa_metadata import parse as parse_metadata
from noaa_client.point_forecast import PointForecast
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
        """Get information about a particular map/geo point from NOAA, via the /points endpoints

        Args:
            latitude: Latitude given as either a float or a string
            longitude: Longitude gives as either a float or a string
        """
        url = f"{self.base_url}/points/{latitude},{longitude}"
        resp = requests.get(url, headers=self.headers, timeout=120)
        resp.raise_for_status()

        meta = parse_metadata(resp.headers)
        json = resp.json()
        return PointInfo(json, meta)

    def point_forecast(self, forecast_office_id: str, grid_x: int, grid_y: int, units: str = "si") -> PointForecast:
        """Get the daily forecast for a particular 2.5km grid square from NOAA

        This is based on the `/gridpoints/{wfo}/{x},{y}/forecast` endpoint from NOAA.
        The arguments for this can be gotten for a lat/long via the `points(lat, long)` method

        Args:
            forecast_office_id: The 3-character weather forecast office identifier
            grid_x: The X offset within the forecast office's grid
            grid_y: the Y offset within the forecast offfice's grid
            units (str, optional): What measurement system to request. Default is SI. Possible values are ["si", "us"]
        """
        url = f"{self.base_url}/gridpoints/{forecast_office_id}/{grid_x},{grid_y}/forecast"
        resp = requests.get(url, params={"units": units}, headers=self.headers, timeout=120)
        resp.raise_for_status()

        meta = parse_metadata(resp.headers)
        return PointForecast(resp.json(), meta)

    # def point_forecast_hourly(self, forecast_office_id: str, grid_x: int, grid_y: int, units: str = "si") -> list:
    #     """Get the hourly forecast for a particular 2.5km grid square from NOAA

    #     This is based on the `/gridpoints/{wfo}/{x},{y}/forecast/hourly` endpoint from NOAA.
    #     The arguments for this can be gotten for a lat/long via the `points(lat, long)` method

    #     Args:
    #         forecast_office_id: The 3-character weather forecast office identifier
    #         grid_x: The X offset within the forecast office's grid
    #         grid_y: the Y offset within the forecast offfice's grid
    #         units (str, optional): What measurement system to request. Default is SI. Possible values are ["si", "us"]
    #     """
    #     url = f"{self.base_url}/gridpoints/{forecast_office_id}/{grid_x},{grid_y}/forecast/hourly"
    #     resp = requests.get(url, headers=self.headers, timeout=120)
    #     resp.raise_for_status()

    #     meta = parse_metadata(resp.headers)
    #     return PointForecastHourly(resp.json(), meta)
