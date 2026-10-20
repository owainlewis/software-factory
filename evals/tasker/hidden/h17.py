import os
from tests.helpers import CliTestCase
class H17(CliTestCase):
    def at(self, day):
        os.environ["TASKER_TODAY"] = day
    def test_stats(self):
        for i, day in enumerate(["2026-03-02", "2026-03-03", "2026-03-04"], start=1):
            self.at(day)
            self.run_cli("add", f"t{i}")
            self.run_cli("done", str(i))
        self.at("2026-03-04")
        self.run_cli("add", "t4")
        self.run_cli("done", "4")
        code, out, _ = self.run_cli("stats")
        self.assertEqual(code, 0)
        self.assertIn("Completed today: 2", out)
        self.assertIn("Streak: 3 days", out)
    def test_no_streak(self):
        _, out, _ = self.run_cli("stats")
        self.assertIn("Completed today: 0", out)
        self.assertIn("Streak: 0 days", out)
