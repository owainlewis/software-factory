#!/usr/bin/env python3
"""Build the Claude Code and Codex packages from src/.

    python3 scripts/build.py           write plugin/ from src/
    python3 scripts/build.py --check   fail if plugin/ is out of date
    python3 scripts/build.py --kit DIR write the plain Claude Code files to DIR/.claude/

src/ is the only place to edit prompts. Claude Code gets one subagent per
role plus a command per entry point (/factory, /review). Codex gets one
skill per entry point whose roles/ folder holds the role prompts, because
Codex plugins cannot ship agents. --kit writes the same Claude Code agents
and commands without the plugin prefix, for factory-kit, which people copy
into their own repo.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = ROOT / "plugin"
NOTE = "<!-- Generated from src/ by scripts/build.py. Edit src/, not this file. -->\n\n"
# Each entry point is a Claude Code command and a Codex skill: (source, metadata, Codex description).
ENTRY_POINTS = {
    "factory": (
        "orchestrator.md",
        "orchestrator.json",
        "Run the software factory on one work ticket: write a verified spec, build it, review "
        "it before pushing, and open a reviewed pull request. Use when asked to run the factory "
        "on a GitHub issue, Linear ticket or PR.",
    ),
    "review": (
        "review.md",
        "review.json",
        "Review the current branch before pushing: a code review, a security review and a risk "
        "classification in parallel, combined into one report. Use when asked to review a change "
        "or a branch.",
    ),
}
GENERATED_DIRS = [OUT / "agents"] + [OUT / "codex" / "skills" / name / "roles" for name in ENTRY_POINTS]


def frontmatter(fields: dict) -> str:
    lines = [f"{key}: {value}" for key, value in fields.items()]
    return "---\n" + "\n".join(lines) + "\n---\n\n"


def expand(text: str) -> str:
    """Fill in the shared snippets that every prompt uses."""
    return text.replace("{{SHELL}}", (SRC / "shell.md").read_text())


def build() -> dict[Path, str]:
    """Return every generated file as {path: content}."""
    roles = json.loads((SRC / "roles.json").read_text())
    files = {}

    for name, role in roles.items():
        body = expand((SRC / "roles" / f"{name}.md").read_text())
        fields = {"name": name, "description": role["description"], **role["claude"]}
        files[OUT / "agents" / f"{name}.md"] = frontmatter(fields) + NOTE + body
        for skill in ENTRY_POINTS:
            files[OUT / "codex" / "skills" / skill / "roles" / f"{name}.md"] = NOTE + body

    for skill, (source, meta_file, codex_description) in ENTRY_POINTS.items():
        text = expand((SRC / source).read_text())
        meta = json.loads((SRC / meta_file).read_text())
        claude = text.replace("{{PLATFORM}}", (SRC / "platform-claude.md").read_text())
        files[OUT / "commands" / f"{skill}.md"] = (
            frontmatter({"description": meta["description"], "argument-hint": meta["argument-hint"]}) + NOTE + claude
        )
        codex = text.replace("{{PLATFORM}}", (SRC / "platform-codex.md").read_text())
        codex = codex.replace("The input: $ARGUMENTS", "The input: what the user gave you.")
        files[OUT / "codex" / "skills" / skill / "SKILL.md"] = (
            frontmatter({"name": skill, "description": codex_description}) + NOTE + codex
        )
    return files


def kit(target: Path) -> dict[Path, str]:
    """Return the Claude Code agents and commands for a plain .claude/ folder."""
    files = {}
    for path, text in build().items():
        if path.parent in (OUT / "agents", OUT / "commands"):
            text = text.replace("software-factory:", "").replace(
                "Generated from src/ by scripts/build.py. Edit src/, not this file.",
                "Generated from owainlewis/software-factory src/ by scripts/build.py --kit. Edit it there.",
            )
            files[target / ".claude" / path.parent.name / path.name] = text
    return files


def leftovers(files: dict[Path, str]) -> list[Path]:
    """Generated-looking files that src/ no longer produces, such as a removed role."""
    return [p for d in GENERATED_DIRS if d.exists() for p in d.glob("*.md") if p not in files]


def main() -> int:
    if "--kit" in sys.argv:
        target = Path(sys.argv[sys.argv.index("--kit") + 1]).resolve()
        for path, text in kit(target).items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        print(f"wrote the kit to {target / '.claude'}")
        return 0
    files = build()
    if "--check" in sys.argv:
        stale = [p for p, text in files.items() if not p.exists() or p.read_text() != text]
        stale += leftovers(files)
        for path in stale:
            print(f"out of date: {path.relative_to(ROOT)}")
        if stale:
            print("Run: python3 scripts/build.py")
        return 1 if stale else 0
    for path in leftovers(files):
        path.unlink()
    for path, text in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    print(f"wrote {len(files)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
