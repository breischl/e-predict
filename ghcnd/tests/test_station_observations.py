import os
import unittest
from datetime import date
from math import nan as NaN
from math import isnan

from ghcnd.station_observations import read_from_dly_file

# pylint: disable=missing-class-docstring,missing-function-docstring


class TestStationDayObservations(unittest.TestCase):

    def test_parse_observations(self):
        filepath = os.path.join(os.path.dirname(__file__), "test_data", "test_daily.dly")
        station_obs = read_from_dly_file(filepath)
        self.assertIsNotNone(station_obs)
        self.assertEqual("USC00050848", station_obs.station_id)
        self.assertEqual(date(2022, 8, 1), station_obs.start_date)
        self.assertEqual(date(2022, 10, 16), station_obs.end_date)

        daily_obs = station_obs.observations
        self.assertEqual(len(daily_obs), 77)
        self.assertEqual(daily_obs[0].date, date(2022, 8, 1))
        self.assertEqual(daily_obs[0].tmax, 339)
        self.assertEqual(daily_obs[0].tmax_decimal, 33.9)
        self.assertEqual(daily_obs[0].tmin_decimal, 15.6)

        self.assertEqual(daily_obs[76].date, date(2022, 10, 16))
        self.assertEqual(daily_obs[76].tmax, 150)
        self.assertEqual(daily_obs[76].tmin, 61)
        self.assertEqual(daily_obs[76].tmax_decimal, 15.0)
        self.assertEqual(daily_obs[76].tmin_decimal, 6.1)

        # Check handling for None values in data
        self.assertEqual(daily_obs[64].date, date(2022, 10, 4))
        self.assertTrue(isnan(daily_obs[64].tmax))
        self.assertTrue(isnan(daily_obs[64].tmin))
        self.assertTrue(isnan(daily_obs[64].tmax_decimal))
        self.assertTrue(isnan(daily_obs[64].tmin_decimal))
