import unittest
from datetime import date

from tasker.quickadd import parse

WED = date(2026, 3, 4)


class QuickAddTest(unittest.TestCase):
    def test_full(self):
        q = parse("Buy milk tomorrow p1 #Shopping @errands", WED)
        self.assertEqual(q.content, "Buy milk")
        self.assertEqual(q.priority, 1)
        self.assertEqual(q.due, date(2026, 3, 5))
        self.assertEqual(q.project, "Shopping")
        self.assertEqual(q.labels, ["errands"])

    def test_plain(self):
        q = parse("Call mum", WED)
        self.assertEqual((q.content, q.priority, q.due, q.project, q.labels), ("Call mum", 4, None, None, []))

    def test_recurrence(self):
        q = parse("Water plants every week", WED)
        self.assertEqual(q.content, "Water plants")
        self.assertEqual(q.recurrence, "every week")
        self.assertEqual(q.due, date(2026, 3, 11))

    def test_several_labels(self):
        q = parse("Email Sam @work @email", WED)
        self.assertEqual(q.labels, ["email", "work"])
