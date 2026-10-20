from tests.helpers import CliTestCase
class H18(CliTestCase):
    def test_time(self):
        self.run_cli("add", "Call Sam tomorrow at 5pm")
        self.run_cli("add", "Lunch today at 12:30")
        self.run_cli("add", "No time tomorrow")
        _, out, _ = self.run_cli("list")
        self.assertIn("2026-03-05 17:00", out)
        self.assertIn("2026-03-04 12:30", out)
        self.assertIn("Call Sam", out)
        self.assertNotIn("at 5pm", out)
        line = next(l for l in out.splitlines() if "No time" in l)
        self.assertIn("2026-03-05", line)
        self.assertNotIn(":", line.split("2026-03-05")[1].split()[0] if line.split("2026-03-05")[1].split() else "")
        _, out, _ = self.run_cli("list", "--filter", "today")
        self.assertIn("Lunch", out)
