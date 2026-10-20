import os
from tests.helpers import CliTestCase
class H13(CliTestCase):
    def test_round_trip(self):
        self.run_cli("add", "Buy milk tomorrow p1 #Shopping @errands")
        self.run_cli("add", "Standup every day #Work @team")
        self.run_cli("add", "Plain")
        _, before, _ = self.run_cli("list")
        path = os.path.join(self._tmp.name, "backup.json")
        code, _, _ = self.run_cli("export", path)
        self.assertEqual(code, 0)
        os.environ["TASKER_DB"] = os.path.join(self._tmp.name, "other.db")
        code, _, _ = self.run_cli("import", path)
        self.assertEqual(code, 0)
        _, after, _ = self.run_cli("list")
        norm = lambda s: sorted(" ".join(l.split()[1:]) for l in s.strip().splitlines())
        self.assertEqual(norm(before), norm(after))
    def test_import_refuses_non_empty(self):
        self.run_cli("add", "x")
        path = os.path.join(self._tmp.name, "b.json")
        self.run_cli("export", path)
        code, _, _ = self.run_cli("import", path)
        self.assertNotEqual(code, 0)
