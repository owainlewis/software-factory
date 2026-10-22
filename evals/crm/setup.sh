#!/bin/bash
# Create a private GitHub repo from the seed and file the 25 tickets.
# Usage: setup.sh <owner/repo> <work-dir>
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=${1:?usage: setup.sh owner/repo work-dir}
WORK=${2:?usage: setup.sh owner/repo work-dir}
rm -rf "$WORK" && cp -R "$HERE/seed" "$WORK" && cd "$WORK"
git init -q -b main && git add -A && git commit -qm "Product brief"
gh repo create "$REPO" --private --source . --push --description "Software Factory eval: CRM from scratch"
python3 - "$HERE/issues.json" <<'PY'
import json, subprocess, sys
for issue in json.load(open(sys.argv[1])):
    cmd = ["gh", "issue", "create", "--title", issue["title"], "--body", issue["body"]]
    for label in issue["labels"]:
        cmd += ["--label", label]
    print(issue["n"], subprocess.run(cmd, capture_output=True, text=True).stdout.strip())
PY
