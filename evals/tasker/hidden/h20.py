from tests.helpers import CliTestCase
class H20(CliTestCase):
    def test_rename(self):
        self.run_cli("add", "x #Work")
        code, _, _ = self.run_cli("rename-project", "Work", "Job")
        self.assertEqual(code, 0)
        _, out, _ = self.run_cli("list")
        self.assertIn("#Job", out)
    def test_errors(self):
        self.run_cli("add", "x #Work")
        self.run_cli("add", "y #Home")
        self.assertEqual(self.run_cli("rename-project", "Nope", "A")[0], 1)
        self.assertEqual(self.run_cli("rename-project", "Work", "Home")[0], 1)
        self.assertEqual(self.run_cli("rename-project", "Inbox", "Main")[0], 1)
        self.assertEqual(self.run_cli("rename-project", "work", "WORK")[0], 0)
