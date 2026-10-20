import unittest
from datetime import date
from tasker.quickadd import parse
from tests.helpers import CliTestCase
class H02(CliTestCase):
    def test_hyphen_label(self):
        q = parse("Write report @high-energy", date(2026, 3, 4))
        self.assertEqual(q.labels, ["high-energy"])
        self.assertEqual(q.content, "Write report")
    def test_cli_label_lookup(self):
        self.run_cli("add", "Write report @deep-work")
        _, out, _ = self.run_cli("label", "deep-work")
        self.assertIn("Write report", out)
