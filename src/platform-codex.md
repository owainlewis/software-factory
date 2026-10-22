## How to run agents (Codex)

- The role prompts are in the `roles/` folder next to this skill: `roles/triage.md`, `roles/implementer.md`, `roles/reviewer.md`, `roles/ux-reviewer.md`, `roles/approver.md`. Use their full paths.
- Spawn one subagent per role with high reasoning effort. Start its task with: `You are the <role> in a software factory. Read <full path to roles/<role>.md> and follow it exactly.` Then add the brief.
- Wait for each agent's report. To answer a waiting agent's questions, send the answers to that same agent thread. Close finished agent threads.
- Ask the user directly in chat.
