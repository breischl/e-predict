import os
import unittest
from datetime import date, datetime

import dotenv

import eia.eia_client


class TestEiaClient(unittest.TestCase):
    def setUp(self):
        dotenv.load_dotenv()

    # skipped unless requested to avoid spamming EIA
    # Run from Powershell like this:     $env:REMOTE_API_TEST="true" ; python -m unittest
    @unittest.skipUnless(os.environ.get("REMOTE_API_TEST"), "Integration test meant to run manually")
    def test_eia_download(self) -> None:
        daily_demand = eia.eia_client.get_electric_demand_hourly(date(2022, 1, 1), date(2022, 1, 2))

        self.assertIsNotNone(daily_demand)
        self.assertEqual(25, len(daily_demand))
        self.assertEqual(0, daily_demand[0].date.hour)
        self.assertEqual(datetime(2022, 1, 1, 0), daily_demand[0].date)
        self.assertEqual(6427, daily_demand[0].demand)
