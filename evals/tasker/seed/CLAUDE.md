# tasker

A small Todoist-style task manager: a CLI over SQLite.

- Python 3.11+, standard library only. No third-party dependencies.
- Run the tests: `python3 -m unittest discover -s tests -v`
- Run the doctests: `python3 -m doctest tasker/*.py`
- Try the CLI: `TASKER_DB=/tmp/t.db python3 -m tasker.cli add "Buy milk tomorrow p1"`
- Tests set `TASKER_TODAY` to fix the date and `TASKER_DB` to a temp file. CLI tests subclass `tests.helpers.CliTestCase`.
- Schema changes go in a new entry at the end of `MIGRATIONS` in `tasker/store.py`. Never edit an old migration.
- Public functions have type hints. Functions with interesting input get a doctest.
- All SQL uses `?` placeholders.
