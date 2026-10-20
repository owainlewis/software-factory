import unittest
from datetime import date, timedelta
from tasker.filters import compile_filter
from tasker.models import Task
WED = date(2026, 3, 4)
def m(q, t): return compile_filter(q, WED, {1: "Inbox"})(t)
class H11(unittest.TestCase):
    def test_days(self):
        self.assertTrue(m("7 days", Task(1, "x", 1, due=WED)))
        self.assertTrue(m("7 days", Task(1, "x", 1, due=WED + timedelta(days=7))))
        self.assertFalse(m("7 days", Task(1, "x", 1, due=WED + timedelta(days=8))))
        self.assertFalse(m("7 days", Task(1, "x", 1, due=WED - timedelta(days=1))))
        self.assertFalse(m("7 days", Task(1, "x", 1)))
    def test_combines(self):
        self.assertTrue(m("3 days & @work", Task(1, "x", 1, due=WED, labels=["work"])))
        self.assertFalse(m("3 days & @work", Task(1, "x", 1, due=WED)))
