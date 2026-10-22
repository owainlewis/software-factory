#!/bin/bash
# Run one ticket through one arm.
# Usage: run.sh <factory|vanilla> <work-dir> <tag> <prompt> [session-id-to-resume]
# The factory arm loads the plugin from $PLUGIN_DIR (default: this repo).
HERE=$(cd "$(dirname "$0")" && pwd)
ARM=$1; WORK=$2; TAG=$3; PROMPT=$4; SESSION=$5
PLUGIN=${PLUGIN_DIR:-$(cd "$HERE/../.." && pwd)}
mkdir -p "$WORK.runs"
cd "$WORK" || exit 1
if [ -z "$SESSION" ]; then git checkout -q main && git pull -q; fi
ARGS=()
[ -n "$SESSION" ] && ARGS+=(--resume "$SESSION")
[ "$ARM" = factory ] && ARGS+=(--plugin-dir "$PLUGIN")
start=$(date +%s)
claude -p "${ARGS[@]}" --permission-mode acceptEdits \
  --allowedTools "Read Edit Write Glob Grep Agent SendMessage Bash(git:*) Bash(gh issue:*) Bash(gh pr:*) Bash(gh api:*) Bash(gh label:*) Bash(gh auth status:*) Bash(gh repo view:*) Bash(gh run:*) Bash(uv:*) Bash(python3:*) Bash(printenv:*) Bash(mkdir:*) Bash(ls:*) Bash(cat:*) Bash(date:*) Bash(tail:*) Bash(head:*) Bash(wc:*) Bash(grep:*) Bash(sort:*) Bash(echo:*) Bash(sed -n:*) Bash(curl http://127.0.0.1:*) Bash(rm .factory/tmp/*)" \
  --output-format json "$PROMPT" > "$WORK.runs/$TAG.json" 2> "$WORK.runs/$TAG.err"
echo "exit=$? secs=$(( $(date +%s) - start ))"
python3 - "$WORK.runs/$TAG.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
print("session:", d.get("session_id"), "| turns:", d.get("num_turns"), "| cost: $%.2f" % (d.get("total_cost_usd") or 0), "| denials:", len(d.get("permission_denials") or []))
for x in d.get("permission_denials") or []:
    print("  DENIED:", x["tool_name"], str(x["tool_input"])[:110].replace("\n", " "))
print(d.get("result"))
PY
