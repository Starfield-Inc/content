import unittest
from datetime import date
from decimal import Decimal

from price_table import age_days, cost

ROW = {"model": "Example", "input": Decimal("2"), "output": Decimal("10"), "checked_on": date(2026, 10, 1)}


class PriceTableTests(unittest.TestCase):
    def test_cost_for_one_million_each(self):
        self.assertEqual(cost(ROW, 1_000_000, 1_000_000), Decimal("12"))

    def test_cost_for_small_usage(self):
        self.assertEqual(cost(ROW, 500_000, 100_000), Decimal("2"))

    def test_age_in_days(self):
        self.assertEqual(age_days(ROW, date(2026, 10, 31)), 30)


if __name__ == "__main__":
    unittest.main()
