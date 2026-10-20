import unittest
from datetime import date

from tasker.filters import FilterError, compile_filter
from tasker.models import Task

WED = date(2026, 3, 4)
PROJECTS = {1: "Inbox", 2: "Work"}


def task(**kwargs) -> Task:
    defaults = {"id": 1, "content": "x", "project_id": 1}
    defaults.update(kwargs)
    return Task(**defaults)


def matches(query: str, t: Task) -> bool:
    return compile_filter(query, WED, PROJECTS)(t)


class FilterTest(unittest.TestCase):
    def test_terms(self):
        self.assertTrue(matches("today", task(due=WED)))
        self.assertTrue(matches("overdue", task(due=date(2026, 3, 1))))
        self.assertTrue(matches("no date", task()))
        self.assertTrue(matches("p1", task(priority=1)))
        self.assertTrue(matches("#work", task(project_id=2)))
        self.assertTrue(matches("@home", task(labels=["home"])))

    def test_operators(self):
        self.assertTrue(matches("p1 & today", task(priority=1, due=WED)))
        self.assertFalse(matches("p1 & today", task(priority=1)))
        self.assertTrue(matches("p1 | p2", task(priority=2)))
        self.assertTrue(matches("!p1", task(priority=3)))
        self.assertTrue(matches("(p1 | p2) & @home", task(priority=2, labels=["home"])))

    def test_errors(self):
        with self.assertRaises(FilterError):
            compile_filter("p1 &", WED, PROJECTS)
        with self.assertRaises(FilterError):
            compile_filter("banana", WED, PROJECTS)
