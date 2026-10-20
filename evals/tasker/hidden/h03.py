import unittest
from datetime import date
from tasker.filters import compile_filter
from tasker.models import Task
WED = date(2026, 3, 4)
def m(q, t): return compile_filter(q, WED, {1: "Inbox"})(t)
class H03(unittest.TestCase):
    def test_and_binds_tighter(self):
        p1 = Task(1, "x", 1, priority=1)
        p2_today = Task(2, "y", 1, priority=2, due=WED)
        p2_none = Task(3, "z", 1, priority=2)
        self.assertTrue(m("p1 | p2 & today", p1))
        self.assertTrue(m("p2 & today | p1", p1))
        self.assertTrue(m("p1 | p2 & today", p2_today))
        self.assertFalse(m("p1 | p2 & today", p2_none))
        self.assertFalse(m("(p1 | p2) & today", p1))
