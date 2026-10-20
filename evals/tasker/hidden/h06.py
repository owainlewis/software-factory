from tests.helpers import CliTestCase
class H06(CliTestCase):
    def test_search(self):
        self.run_cli("add", "Buy Milk")
        self.run_cli("add", "Call mum")
        self.run_cli("add", "milkshake done")
        self.run_cli("done", "3")
        code, out, _ = self.run_cli("search", "milk")
        self.assertEqual(code, 0)
        self.assertIn("Buy Milk", out)
        self.assertNotIn("Call mum", out)
        self.assertNotIn("milkshake", out)
