import os
import unittest

from dotenv import load_dotenv

from noaa_client.forecast_client import ForecastClient


# pylint: disable=missing-class-docstring,missing-function-docstring
class TestForecastClient(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        self.client = ForecastClient(
            user_agent=os.environ.get("NOAA_USER_AGENT"))

    def test_points(self) -> None:
        point_info = self.client.points("40.242056", "-104.819259")
        self.assertEqual(
            point_info.id, "https://api.weather.gov/points/40.2421,-104.8193")
        self.assertEqual(point_info.grid_id, "BOU")
        self.assertEqual(point_info.latitude, 40.216683000000003)
        self.assertEqual(point_info.longitude, -104.824077)
        self.assertEqual(point_info.grid_x, 70)
        self.assertEqual(point_info.grid_y, 83)
