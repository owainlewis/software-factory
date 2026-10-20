import json
import threading
import unittest
import urllib.request
import urllib.error
from tasker.api import make_server
from tasker.store import Store
class H19(unittest.TestCase):
    def setUp(self):
        self.store = Store()
        self.server = make_server(self.store, "127.0.0.1", 0)
        self.port = self.server.server_address[1]
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
    def req(self, method, path, body=None):
        data = json.dumps(body).encode() if body is not None else None
        r = urllib.request.Request(f"http://127.0.0.1:{self.port}{path}", data=data, method=method,
                                   headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(r) as resp:
                return resp.status, json.loads(resp.read() or b"null")
        except urllib.error.HTTPError as e:
            return e.code, None
    def test_flow(self):
        status, _ = self.req("POST", "/tasks", {"text": "Buy milk p1"})
        self.assertIn(status, (200, 201))
        status, tasks = self.req("GET", "/tasks")
        self.assertEqual(status, 200)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["content"], "Buy milk")
        tid = tasks[0]["id"]
        status, _ = self.req("POST", f"/tasks/{tid}/done")
        self.assertIn(status, (200, 204))
        _, tasks = self.req("GET", "/tasks")
        self.assertEqual(tasks, [])
    def test_404(self):
        status, _ = self.req("POST", "/tasks/999/done")
        self.assertEqual(status, 404)
