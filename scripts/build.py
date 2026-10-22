#!/usr/bin/env python3
"""Build the Claude Code and Codex packages from src/.

    python3 scripts/build.py           write plugin/ from src/
    python3 scripts/build.py --check   fail if plugin/ is out of date

src/ is the only place to edit prompts. Claude Code gets one subagent per
role plus a /factory command. Codex gets one `factory` skill whose roles/
folder holds the role prompts, because Codex plugins cannot ship agents.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = ROOT / "plugin"
NOTE = "<!-- Generated from src/ by scripts/build.py. Edit src/, not this file. -->\n\n"
CODEX_DESCRIPTION = (
    "Run the software factory: plan a ticket or goal, write a verified spec, build it, "
    "review it before pushing, and merge low-risk work. Use when asked to run the factory "
    "on a GitHub issue, Linear ticket, PR or goal."
)


def frontmatter(fields: dict) -> str:
    lines = [f"{key}: {value}" for key, value in fields.items()]
    return "---\n" + "\n".join(lines) + "\n---\n\n"


def build() -> dict[Path, str]:
    """Return every generated file as {path: content}."""
    roles = json.loads((SRC / "roles.json").read_text())
    orchestrator = (SRC / "orchestrator.md").read_text()
    meta = json.loads((SRC / "orchestrator.json").read_text())
    files = {}

    for name, role in roles.items():
        body = (SRC / "roles" / f"{name}.md").read_text()
        fields = {"name": name, "description": role["description"], **role["claude"]}
        files[OUT / "agents" / f"{name}.md"] = frontmatter(fields) + NOTE + body
        files[OUT / "codex" / "skills" / "factory" / "roles" / f"{name}.md"] = NOTE + body

    claude = orchestrator.replace("{{PLATFORM}}", (SRC / "platform-claude.md").read_text())
    files[OUT / "commands" / "factory.md"] = (
        frontmatter({"description": meta["description"], "argument-hint": meta["argument-hint"]}) + NOTE + claude
    )

    codex = orchestrator.replace("{{PLATFORM}}", (SRC / "platform-codex.md").read_text())
    codex = codex.replace("The input: $ARGUMENTS", "The input: the ticket, PR or goal the user gave you.")
    files[OUT / "codex" / "skills" / "factory" / "SKILL.md"] = (
        frontmatter({"name": "factory", "description": CODEX_DESCRIPTION}) + NOTE + codex
    )
    return files


def main() -> int:
    files = build()
    if "--check" in sys.argv:
        stale = [p for p, text in files.items() if not p.exists() or p.read_text() != text]
        for path in stale:
            print(f"out of date: {path.relative_to(ROOT)}")
        if stale:
            print("Run: python3 scripts/build.py")
        return 1 if stale else 0
    for path, text in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    print(f"wrote {len(files)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
