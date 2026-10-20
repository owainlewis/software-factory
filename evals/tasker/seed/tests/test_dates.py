import unittest
from datetime import date

from tasker.dates import parse_due

WED = date(2026, 3, 4)


class ParseDueTest(unittest.TestCase):
    def test_today_and_tomorrow(self):
        self.assertEqual(parse_due("today", WED), WED)
        self.assertEqual(parse_due("Tomorrow", WED), date(2026, 3, 5))

    def test_weekday(self):
        self.assertEqual(parse_due("friday", WED), date(2026, 3, 6))
        self.assertEqual(parse_due("monday", WED), date(2026, 3, 9))

    def test_in_days_and_weeks(self):
        self.assertEqual(parse_due("in 3 days", WED), date(2026, 3, 7))
        self.assertEqual(parse_due("in 1 week", WED), date(2026, 3, 11))

    def test_month_day(self):
        self.assertEqual(parse_due("mar 10", WED), date(2026, 3, 10))
        self.assertEqual(parse_due("jan 5", WED), date(2027, 1, 5))

    def test_iso(self):
        self.assertEqual(parse_due("2026-12-25", WED), date(2026, 12, 25))

    def test_unknown(self):
        self.assertIsNone(parse_due("someday", WED))
