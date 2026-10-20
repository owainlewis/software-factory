import contextlib
import io
import os
import tempfile
import unittest
from unittest import mock

from tasker import cli


class CliTestCase(unittest.TestCase):
    """Runs the CLI against a fresh database with a fixed date."""

    today = "2026-03-04"  # a Wednesday

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        env = {"TASKER_DB": os.path.join(self._tmp.name, "test.db"), "TASKER_TODAY": self.today}
        patcher = mock.patch.dict(os.environ, env)
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_cli(self, *argv: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = cli.main(list(argv))
        return code, out.getvalue(), err.getvalue()
