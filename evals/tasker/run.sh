#!/bin/bash
# Run the factory once in the eval checkout and print cost, denials and the result.
# Usage: run.sh <tag> <prompt> [session-id-to-resume]
HERE=$(cd "$(dirname "$0")" && pwd)
# The checkout must live outside the plugin folder: Claude Code refuses edits inside a loaded plugin.
WORK=${EVAL_WORK:-${TMPDIR:-/tmp}/software-factory-eval}
PLUGIN=$(cd "$HERE/../.." && pwd)
mkdir -p "$WORK.runs"
cd "$WORK" || exit 1
if [ -z "$3" ]; then git checkout -q main && git pull -q; fi
RESUME=()
[ -n "$3" ] && RESUME=(--resume "$3")
start=$(date +%s)
claude -p "${RESUME[@]}" --plugin-dir "$PLUGIN" --permission-mode acceptEdits \
  --allowedTools "Read Edit Write Glob Grep Agent SendMessage Bash(git:*) Bash(gh issue:*) Bash(gh pr:*) Bash(gh api:*) Bash(gh label:*) Bash(gh auth status:*) Bash(gh repo view:*) Bash(python3:*) Bash(printenv:*) Bash(mkdir:*) Bash(ls:*) Bash(cat:*) Bash(date:*) Bash(tail:*) Bash(head:*) Bash(wc:*) Bash(grep:*) Bash(sort:*) Bash(echo:*) Bash(sed -n:*) Bash(rm .factory/tmp/*)" \
  --output-format json "$2" > "$WORK.runs/$1.json" 2> "$WORK.runs/$1.err"
echo "exit=$? secs=$(( $(date +%s) - start ))"
python3 - "$WORK.runs/$1.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
print("session:", d.get("session_id"), "| turns:", d.get("num_turns"), "| cost: $%.2f" % (d.get("total_cost_usd") or 0), "| denials:", len(d.get("permission_denials") or []))
for x in d.get("permission_denials") or []:
    print("  DENIED:", x["tool_name"], str(x["tool_input"])[:110].replace("\n", " "))
print(d.get("result"))
PY
