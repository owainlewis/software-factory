from tests.helpers import CliTestCase
class H14(CliTestCase):
    def test_undo(self):
        self.run_cli("add", "Task A")
        self.run_cli("done", "1")
        code, _, _ = self.run_cli("undo")
        self.assertEqual(code, 0)
        _, out, _ = self.run_cli("list")
        self.assertIn("Task A", out)
    def test_undo_recurring(self):
        self.run_cli("add", "Standup every day")
        self.run_cli("done", "1")
        self.run_cli("undo")
        _, out, _ = self.run_cli("list")
        self.assertIn("2026-03-04", out)
    def test_nothing(self):
        code, _, _ = self.run_cli("undo")
        self.assertEqual(code, 1)
