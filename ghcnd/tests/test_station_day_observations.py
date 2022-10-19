import unittest
import os
from datetime import date
from ghcnd.station_day_observations import parse_from_dly_text

# pylint: disable=missing-class-docstring,missing-function-docstring


class TestStationDayObservations(unittest.TestCase):

    def setUp(self):
        filepath = os.path.join(os.path.dirname(__file__), "test_data", "test_daily.dly")
        with open(filepath, "r", encoding="utf-8") as file:
            self.daily_text = file.read()

    def test_parse_observations(self):
        obs = parse_from_dly_text(self.daily_text)
        self.assertIsNotNone(obs)

        self.assertEqual(len(obs), 92)
        self.assertEqual(obs[0].date, date(2022, 8, 1))
        self.assertEqual(obs[0].temp_max, 339)
        self.assertEqual(obs[0].temp_min, 156)
        self.assertEqual(obs[30].temp_max, 322)
        self.assertEqual(obs[30].temp_min, 139)
        self.assertEqual(obs[76].date, date(2022, 10, 16))
        self.assertEqual(obs[76].temp_max, 150)
        self.assertEqual(obs[76].temp_min, 61)
