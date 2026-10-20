from tests.helpers import CliTestCase
class H10(CliTestCase):
    def test_delete_removes_its_tasks(self):
        self.run_cli("add", "work thing #Work")
        self.run_cli("add", "home thing #Home")
        code, out, _ = self.run_cli("delete-project", "Work")
        self.assertEqual(code, 0)
        self.assertIn("1", out)
        _, out, _ = self.run_cli("list")
        self.assertNotIn("work thing", out)
        self.assertIn("home thing", out)
        self.assertNotIn("#?", out)
