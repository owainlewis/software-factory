# Evals

End-to-end tests for the factory: a real repo, real GitHub issues, and acceptance tests the factory never sees.

## tasker

`tasker/` is a small Todoist-style CLI (Python, standard library, SQLite) with 20 issues:

- **Bugs with planted causes:** date parsing, label parsing, filter precedence, a month-end crash, SQL injection.
- **Traps:** a duplicate issue, a question that is not a work request, a bug report that blames the wrong thing, and a vague performance complaint.
- **Features from S to L:** search, recurrence, export/import, undo, JSON output, subtasks, stats, due times and an HTTP API.

Each issue with code to check has a hidden test in `tasker/hidden/`. `answers.md` holds the product owner's answers for when the factory asks questions, so runs stay comparable.

### Run it

```bash
evals/tasker/setup.sh you/factory-tasker-eval
evals/tasker/run.sh r01 "/software-factory:factory https://github.com/you/factory-tasker-eval/issues/1"
evals/tasker/grade.sh 1 <pr-number>
```

The checkout goes in `$EVAL_WORK` (default `$TMPDIR/software-factory-eval`). It must be outside this repo, because Claude Code refuses edits inside a loaded plugin's folder.

If the run stops with a question, answer it from `answers.md` and resume with the session id it printed: `run.sh r01b "<answer>" <session-id>`. Merge each PR that passes before the next run, so later issues build on earlier ones. At the end, copy every hidden test into the checkout's `tests/` and run them together, to catch a later PR breaking an earlier one.

### Results

[`tasker/RESULTS.md`](tasker/RESULTS.md) has both passes.

| | First pass (prompts changing) | Clean pass (frozen) |
|---|---|---|
| Hidden tests on final main | 18/18 | 18/18 |
| Human saves | 2 | 1 |
| Stops to ask the user | 10 | 3, plus one spec interview |
| Permission denials | 18 | 2 |
| Total cost | $60.48 | $47.22 |
