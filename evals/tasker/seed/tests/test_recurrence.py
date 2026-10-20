import unittest
from datetime import date

from tasker.recurrence import next_due


class NextDueTest(unittest.TestCase):
    def test_rules(self):
        d = date(2026, 3, 4)
        self.assertEqual(next_due("every day", d), date(2026, 3, 5))
        self.assertEqual(next_due("every week", d), date(2026, 3, 11))
        self.assertEqual(next_due("every 3 days", d), date(2026, 3, 7))
        self.assertEqual(next_due("every 2 weeks", d), date(2026, 3, 18))
        self.assertEqual(next_due("every month", d), date(2026, 4, 4))
        self.assertEqual(next_due("every friday", d), date(2026, 3, 6))

    def test_december(self):
        self.assertEqual(next_due("every month", date(2026, 12, 10)), date(2027, 1, 10))

    def test_unknown(self):
        with self.assertRaises(ValueError):
            next_due("every blue moon", date(2026, 3, 4))
