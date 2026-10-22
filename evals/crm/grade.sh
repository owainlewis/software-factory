#!/bin/bash
# Run the builder's tests and the hidden tests up to ticket N on a branch or PR.
# Usage: grade.sh <work-dir> <ticket-number> [pr-number]
HERE=$(cd "$(dirname "$0")" && pwd)
WORK=$1; N=$2; PR=$3
cd "$WORK" || exit 1
git fetch -q origin
if [ -n "$PR" ]; then git checkout -q --detach "origin/$(gh pr view "$PR" --json headRefName -q .headRefName)" || exit 1
else git checkout -q main && git pull -q; fi
rm -rf .hidden && mkdir .hidden && cp "$HERE/hidden/conftest.py" .hidden/
for j in $(seq 1 "$N"); do i=$(printf "%02d" "$j"); [ -f "$HERE/hidden/test_h$i.py" ] && cp "$HERE/hidden/test_h$i.py" .hidden/; done
echo "== builder tests"; uv run pytest -q 2>&1 | tail -1
echo "== hidden tests up to $N"; PYTHONPATH=. uv run --with pytest --with httpx pytest -q -p no:cacheprovider .hidden 2>&1 | grep -E "passed|failed|error" | tail -3
echo "== failing"; PYTHONPATH=. uv run --with pytest --with httpx pytest -q -p no:cacheprovider .hidden 2>&1 | grep -E "^FAILED|^ERROR" | head -10
rm -rf .hidden
[ -n "$PR" ] && { echo "== PR"; gh pr view "$PR" --json title,labels,state --jq '.title + " | " + .state + " | " + (.labels|map(.name)|join(","))'; git diff --stat origin/main...HEAD | tail -1; }
git checkout -q main
