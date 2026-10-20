import unittest
from datetime import date
from tasker.recurrence import next_due
from tasker.quickadd import parse
class H08(unittest.TestCase):
    def test_next_weekday(self):
        self.assertEqual(next_due("every weekday", date(2026, 3, 6)), date(2026, 3, 9))   # Fri -> Mon
        self.assertEqual(next_due("every weekday", date(2026, 3, 4)), date(2026, 3, 5))   # Wed -> Thu
        self.assertEqual(next_due("every weekday", date(2026, 3, 7)), date(2026, 3, 9))   # Sat -> Mon
    def test_quick_add(self):
        q = parse("Standup every weekday", date(2026, 3, 4))
        self.assertEqual(q.recurrence, "every weekday")
        self.assertEqual(q.content, "Standup")
        self.assertIsNotNone(q.due)
        self.assertLess(q.due.weekday(), 5)
