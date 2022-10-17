import os
import re
import unittest

import responses
from dotenv import load_dotenv
from responses import _recorder
from noaa_client.forecast_client import ForecastClient

# pylint: disable=missing-class-docstring,missing-function-docstring


class TestForecastClientGridpointForecasts(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        self.client = ForecastClient(
            user_agent=os.environ.get("NOAA_USER_AGENT"))

    # skipped unless requested to avoid spamming NOAA
    # Run from Powershell like this:     $env:REMOTE_API_TEST="true" ; python -m unittest
    @unittest.skipUnless(os.environ.get("REMOTE_API_TEST"), "Integration test meant to run manually")
    @_recorder.record(file_path="noaa_client/tests/recorded_responses/test_gridpoint_forecast_integration.toml")
    def test_gridpoint_forecast_integration(self) -> None:
        """Integration test that hits the live NOAA endpoint"""
        forecast = self.client.point_forecast("BOU", 70, 83)
        self.assertIsNotNone(forecast.json)
        self.assertIsNotNone(forecast.meta)
        self.assertTrue(forecast.periods)

    @responses.activate
    def test_request_fields_and_parsing(self) -> None:
        """Test that request URL escaping and headers are correct. Also basic response parsing."""
        responses._add_from_file("noaa_client/tests/test_data/gridpoint_forecast.toml")  # pylint: disable=protected-access

        forecast = self.client.point_forecast("BOU", 70, 83, units="us")

        req = responses.calls[0].request
        self.assertEqual(req.url, "https://api.weather.gov/gridpoints/BOU/70,83/forecast?units=us")
        self.assertEqual(req.headers["Accept"], "application/geo+json")
        self.assertEqual(os.environ.get("NOAA_USER_AGENT"), req.headers["User-Agent"])

        self.assertIsNotNone(forecast)
        self.assertIsNotNone(forecast.periods)
        self.assertEqual(forecast.updated.year, 2022)

        for period in forecast.periods:
            self.assertIsNotNone(period.number)
            self.assertEqual(period.start_time.year, 2022)
            self.assertEqual(period.end_time.year, 2022)
            self.assertTrue(period.start_time < period.end_time)
            self.assertGreaterEqual(period.temperature, 0)

        periods = list(forecast.periods)
        self.assertTrue(periods[0].is_day_time)
        self.assertFalse(periods[1].is_day_time)
