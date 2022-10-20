import unittest
import os
from datetime import date
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
        self.assertEqual(daily_obs[0].temp_max, 339)
        self.assertEqual(daily_obs[0].temp_min, 156)
        self.assertEqual(daily_obs[30].temp_max, 322)
        self.assertEqual(daily_obs[30].temp_min, 139)
        self.assertEqual(daily_obs[76].date, date(2022, 10, 16))
        self.assertEqual(daily_obs[76].temp_max, 150)
        self.assertEqual(daily_obs[76].temp_min, 61)
