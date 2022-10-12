import os
import re
import unittest

import responses
from dotenv import load_dotenv
from noaa_client.forecast_client import ForecastClient
from responses import _recorder


# pylint: disable=missing-class-docstring,missing-function-docstring
class TestForecastClient(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        self.client = ForecastClient(
            user_agent=os.environ.get("NOAA_USER_AGENT"))

    # skipped unless requested to avoid spamming NOAA
    # Run from Powershell like this:     $env:REMOTE_API_TEST="true" ; python -m unittest
    @unittest.skipUnless(os.environ.get("REMOTE_API_TEST"), "Integration test meant to run manually")
    @_recorder.record(file_path="noaa_client/tests/recorded_responses/test_points_integration.toml")
    def test_points_integration(self) -> None:
        """Integration test that hits the live NOAA endpoint"""
        point_info = self.client.points("40.242056", "-104.819259")
        self.assertEqual(
            point_info.id, "https://api.weather.gov/points/40.2421,-104.8193")
        self.assertEqual(point_info.grid_id, "BOU")
        self.assertEqual(point_info.latitude, 40.216683000000003)
        self.assertEqual(point_info.longitude, -104.824077)
        self.assertEqual(point_info.grid_x, 70)
        self.assertEqual(point_info.grid_y, 83)

    @responses.activate
    def test_request_fields_and_parsing(self) -> None:
        """Test that request URL escaping and headers are correct. Also basic response parsing."""
        url_re = re.compile(re.escape("https://api.weather.gov/points/") + ".*")
        _ = responses.get(url_re, json={
            "properties": {
                "@id": "https://api.weather.gov/points/40.2421,-104.8193",
                "gridId": "BOU",
                "gridX": 70,
                "gridY": 83,
                "relativeLocation":
                {"geometry": {
                    "coordinates": [-104.824077,
                                    40.216683000000003]
                }}
            }
        })

        point_info = self.client.points("40.242056", "-104.819259")

        req = responses.calls[0].request
        self.assertEqual(req.url, "https://api.weather.gov/points/40.242056,-104.819259")
        self.assertEqual(req.headers["Accept"], "application/geo+json")
        self.assertEqual(os.environ.get("NOAA_USER_AGENT"), req.headers["User-Agent"])

        self.assertEqual(
            point_info.id, "https://api.weather.gov/points/40.2421,-104.8193")
        self.assertEqual(point_info.grid_id, "BOU")
        self.assertEqual(point_info.latitude, 40.216683000000003)
        self.assertEqual(point_info.longitude, -104.824077)
        self.assertEqual(point_info.grid_x, 70)
        self.assertEqual(point_info.grid_y, 83)
