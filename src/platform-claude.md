## How to run agents (Claude Code)

- Spawn each role with the Agent tool, `subagent_type: software-factory:<role>` (for example `software-factory:triage`), and a `name`.
- Ask the user with AskUserQuestion, or plain text for open questions. Send answers to a waiting agent with SendMessage to its name.
- Shell commands go through Bash. Permission rules match the first word of a command, which is why each call is one plain command.
