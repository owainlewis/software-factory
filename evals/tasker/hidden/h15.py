import json
from tests.helpers import CliTestCase
class H15(CliTestCase):
    def test_json(self):
        self.run_cli("add", "Buy milk tomorrow p1 #Shopping @errands")
        self.run_cli("add", "Other")
        code, out, _ = self.run_cli("list", "--json", "--filter", "p1")
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(len(data), 1)
        t = data[0]
        self.assertEqual(t["content"], "Buy milk")
        self.assertEqual(t["priority"], 1)
        self.assertEqual(t["due"], "2026-03-05")
        self.assertEqual(t["project"], "Shopping")
        self.assertEqual(t["labels"], ["errands"])
        self.assertIn("recurrence", t)
        self.assertIn("id", t)
    def test_empty(self):
        _, out, _ = self.run_cli("list", "--json")
        self.assertEqual(json.loads(out), [])
