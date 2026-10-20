from tests.helpers import CliTestCase


class CliTest(CliTestCase):
    def test_add_and_list(self):
        code, out, _ = self.run_cli("add", "Buy milk tomorrow p1 #Shopping @errands")
        self.assertEqual(code, 0)
        self.assertIn("Added task 1", out)
        _, out, _ = self.run_cli("list")
        self.assertIn("Buy milk", out)
        self.assertIn("2026-03-05", out)
        self.assertIn("#Shopping", out)
        self.assertIn("@errands", out)

    def test_list_sorted_by_priority(self):
        self.run_cli("add", "Low")
        self.run_cli("add", "High p1")
        _, out, _ = self.run_cli("list")
        self.assertLess(out.index("High"), out.index("Low"))

    def test_filter(self):
        self.run_cli("add", "A today p1")
        self.run_cli("add", "B tomorrow")
        _, out, _ = self.run_cli("list", "--filter", "today")
        self.assertIn("A", out)
        self.assertNotIn("B", out)

    def test_bad_filter(self):
        code, _, err = self.run_cli("list", "--filter", "p1 &")
        self.assertEqual(code, 1)
        self.assertIn("error", err)

    def test_done(self):
        self.run_cli("add", "Task")
        code, out, _ = self.run_cli("done", "1")
        self.assertEqual(code, 0)
        _, out, _ = self.run_cli("list")
        self.assertNotIn("Task", out)

    def test_done_recurring(self):
        self.run_cli("add", "Standup every day")
        _, out, _ = self.run_cli("done", "1")
        self.assertIn("next due 2026-03-05", out)

    def test_projects(self):
        self.run_cli("add", "x #Work")
        _, out, _ = self.run_cli("projects")
        self.assertEqual(out.split(), ["Inbox", "Work"])

    def test_delete_project(self):
        self.run_cli("add", "x #Work")
        code, out, _ = self.run_cli("delete-project", "Work")
        self.assertEqual(code, 0)
        code, _, err = self.run_cli("delete-project", "Inbox")
        self.assertEqual(code, 1)

    def test_label(self):
        self.run_cli("add", "x @home")
        self.run_cli("add", "y @work")
        _, out, _ = self.run_cli("label", "home")
        self.assertIn("x", out)
        self.assertNotIn("  y  ", out)
