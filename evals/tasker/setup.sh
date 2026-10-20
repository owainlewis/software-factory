#!/bin/bash
# Create a private GitHub repo from the seed app and file the 20 issues.
# Usage: setup.sh <owner/repo>
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
# The checkout must live outside the plugin folder: Claude Code refuses edits inside a loaded plugin.
WORK=${EVAL_WORK:-${TMPDIR:-/tmp}/software-factory-eval}
REPO=${1:?usage: setup.sh owner/repo}
rm -rf "$WORK" && cp -R "$HERE/seed" "$WORK" && cd "$WORK"
git init -q -b main && git add -A && git commit -qm "Initial tasker"
gh repo create "$REPO" --private --source . --push --description "Software Factory eval: tasker"
python3 - "$HERE/issues.json" <<'PY'
import json, subprocess, sys
for issue in json.load(open(sys.argv[1])):
    cmd = ["gh", "issue", "create", "--title", issue["title"], "--body", issue["body"]]
    for label in issue["labels"]:
        cmd += ["--label", label]
    print(issue["n"], subprocess.run(cmd, capture_output=True, text=True).stdout.strip())
PY
