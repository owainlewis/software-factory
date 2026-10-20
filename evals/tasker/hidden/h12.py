import time
import unittest
from tasker.store import Store
from tasker.models import Task
class H12(unittest.TestCase):
    def test_list_query_count(self):
        s = Store()
        for i in range(500):
            s.add_task(Task(None, f"t{i}", 1, labels=["a", "b"]))
        queries = []
        s.conn.set_trace_callback(queries.append)
        tasks = s.list_tasks()
        s.conn.set_trace_callback(None)
        self.assertEqual(len(tasks), 500)
        self.assertEqual(tasks[0].labels, ["a", "b"])
        self.assertLessEqual(len([q for q in queries if q.strip().upper().startswith("SELECT")]), 3)
    def test_list_speed(self):
        s = Store()
        for i in range(5000):
            s.add_task(Task(None, f"t{i}", 1, labels=["a"]))
        start = time.perf_counter()
        s.list_tasks()
        self.assertLess(time.perf_counter() - start, 0.5)
