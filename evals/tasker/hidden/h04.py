import unittest
from datetime import date
from tasker.recurrence import next_due
class H04(unittest.TestCase):
    def test_clamps(self):
        self.assertEqual(next_due("every month", date(2026, 1, 31)), date(2026, 2, 28))
        self.assertEqual(next_due("every month", date(2028, 1, 31)), date(2028, 2, 29))
        self.assertEqual(next_due("every month", date(2026, 3, 31)), date(2026, 4, 30))
        self.assertEqual(next_due("every month", date(2026, 12, 31)), date(2027, 1, 31))
