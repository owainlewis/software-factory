from tasker.store import Store
from tasker.models import Task
from tests.helpers import CliTestCase
class H09(CliTestCase):
    def test_quote_label(self):
        s = Store()
        s.add_task(Task(None, "x", 1, labels=["it's"]))
        self.assertEqual([t.content for t in s.tasks_with_label("it's")], ["x"])
    def test_injection(self):
        s = Store()
        s.add_task(Task(None, "secret", 1, labels=["a"]))
        self.assertEqual(s.tasks_with_label("x' OR '1'='1"), [])
    def test_cli(self):
        code, _, _ = self.run_cli("label", "it's")
        self.assertEqual(code, 0)
