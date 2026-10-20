#!/bin/bash
# Run the visible and hidden tests against a factory PR, then show its labels and commits.
# Usage: grade.sh <issue-number> <pr-number>
HERE=$(cd "$(dirname "$0")" && pwd)
# The checkout must live outside the plugin folder: Claude Code refuses edits inside a loaded plugin.
WORK=${EVAL_WORK:-${TMPDIR:-/tmp}/software-factory-eval}
cd "$WORK" || exit 1
N=$(printf "%02d" "$1")
git fetch -q origin && git checkout -q --detach "origin/$(gh pr view "$2" --json headRefName -q .headRefName)" || exit 1
echo "== visible tests"; python3 -m unittest discover -s tests 2>&1 | tail -1
echo "== doctests"; python3 -m doctest tasker/*.py && echo ok
if [ -f "$HERE/hidden/h$N.py" ]; then
  cp "$HERE/hidden/h$N.py" "tests/test_hidden_$N.py"
  echo "== hidden h$N"; python3 -m unittest -v "tests.test_hidden_$N" 2>&1 | grep -E "ok$|FAIL|ERROR|^Ran|^OK|^FAILED"
  rm "tests/test_hidden_$N.py"
fi
echo "== diff"; git diff --stat origin/main...HEAD | tail -1
echo "== PR"; gh pr view "$2" --json title,labels --jq '.title + " | " + (.labels|map(.name)|join(","))'
echo "== commits"; gh pr view "$2" --json commits --jq '.commits[]|"* "+.messageHeadline'
git checkout -q main
