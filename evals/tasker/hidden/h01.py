import unittest
from datetime import date
from tasker.dates import parse_due
MON = date(2026, 3, 2)
class H01(unittest.TestCase):
    def test_next_monday_on_monday(self):
        self.assertEqual(parse_due("next monday", MON), date(2026, 3, 9))
    def test_plain_monday_on_monday(self):
        self.assertEqual(parse_due("monday", MON), MON)
    def test_next_never_today(self):
        for offset in range(7):
            today = date(2026, 3, 2 + offset)
            for wd in ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]:
                self.assertNotEqual(parse_due("next " + wd, today), today)
