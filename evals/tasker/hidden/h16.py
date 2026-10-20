from tests.helpers import CliTestCase
class H16(CliTestCase):
    def test_subtasks(self):
        self.run_cli("add", "Bake cake")
        code, _, _ = self.run_cli("add", "--parent", "1", "Buy flour")
        self.assertEqual(code, 0)
        self.run_cli("add", "Other p1")
        _, out, _ = self.run_cli("list")
        lines = out.splitlines()
        parent = next(i for i, l in enumerate(lines) if "Bake cake" in l)
        child = next(i for i, l in enumerate(lines) if "Buy flour" in l)
        self.assertEqual(child, parent + 1)
        indent = lambda l: len(l) - len(l.lstrip())
        self.assertGreater(indent(lines[child]), indent(lines[parent]))
    def test_complete_parent(self):
        self.run_cli("add", "Bake cake")
        self.run_cli("add", "--parent", "1", "Buy flour")
        self.run_cli("done", "1")
        _, out, _ = self.run_cli("list")
        self.assertNotIn("Buy flour", out)
    def test_bad_parent(self):
        code, _, _ = self.run_cli("add", "--parent", "99", "x")
        self.assertNotEqual(code, 0)
