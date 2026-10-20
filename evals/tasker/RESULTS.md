# tasker eval: run 1 (2026-10-20)

Prompts were changed between runs, so each row reflects the plugin as it was at that run. "Hidden" is the hidden acceptance tests passed. Quality and Process are scored 1 to 5 by hand. Cost includes every resume for that issue.

| Run | Issue | Kind | Hidden | Quality | Process | Cost | Denials | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | #1 next monday | bug | 3/3 | 5 | 3 | $1.90 | 12 | Good question (A/B). Minimal fix. Denials from cd/export/env prefix/echo chains. Left checkout on branch. |
| 2 | #2 hyphen labels | bug | 2/2 | 5 | 3 | $1.75 | 1 | Missed #5 as duplicate and #9 for SQL. Asked a trivial edge-case question. Shell fix cut denials 12 to 1. Branch restore works. |
| 3 | #3 filter precedence | bug | 1/1 | 5 | 5 | $1.08 | 1 | Clean grammar split, no questions. Reviewer flagged a weak assertion as minor; orchestrator rightly did not loop. |
| 4 | #4 monthly 31st | bug | 1/1 | 5 | 4 | $1.76 | 1 | Excellent 4-option question. Triage posted an assumed answer on the issue before the user chose. |
| 5 | #5 duplicate | duplicate | n/a | 5 | 5 | $0.46 | 0 | Found dup of closed #2, checked fix on main, touched nothing, pointed at #9. Dup-search fix works. |
| 6 | #6 search | feature S | 1/1 | 4 | 5 | $1.12 | 1 | Shared list_order helper, casefold. Search takes one word while add takes many (minor UX). Multi-line python -c denied. |
| 7 | #7 question | question | n/a | 4 | 4 | $0.49 | 0 | Correct answer, evidence, no side effects. Missed that open #8 already tracks the feature (research mode skipped dup check). |
| 8 | #8 every weekday | feature S | 2/2 | 4 | 5 | $1.30 | 0 | Good weekend assumptions, linked #7. README left stale; reviewer called it minor. |
| 9 | #9 SQL injection | security bug | 3/3 | 5 | 5 | $1.15 | 1 | Root cause (placeholder), injection test, audited other queries. Denial traced to triage lacking Write tool. |
| 10 | #10 misdescribed delete | bug | 1/1 | 5 | 5 | $1.91 | 1 | Corrected the wrong report, real cause (FKs off). Help text updated. Reviewer mutation-tested. Flagged old orphans as follow-up. |
| 11 | #11 N days filter | feature S | 2/2 | 5 | 3 | $2.60 | 0 | Asked 7 'defaults' it should have assumed. First revision round (huge-N crash), resumed same implementer. README updated. |
| 12 | #12 vague perf | perf | 2/2 | 3 then 5 | 4 | $3.98 | 0 | Found N+1 from vague report, measured. First design passed SQL text to a helper; reviewer called it minor. Human review fixed it. Added repo-rule and simplicity rules. |
| 13 | #13 export/import | feature M | 2/2 | 5 | 4 | $3.53 | 0 | One real data-loss question, rest as assumptions (orchestrator fix works). Clean transfer module. Review round chased crafted inputs; added likelihood rule. |
| 14 | #14 undo | feature M | 3/3 | 4 | 5 | $1.70 | 0 | No questions: safe defaults became PR assumptions. New migration. Caught SQLite id-reuse hazard. Latent double commit left as minor. |
| 15 | #15 list --json | feature S | 2/2 | 5 | 5 | $1.30 | 0 | No questions, shared record builder with export, README updated. |
| 16 | #16 subtasks | feature L | 3/3 | 5 | 5 | $9.63 | 0 | Good question, needs_human finding posted on PR per template, 2 review rounds, migration upgrade checked. Too expensive: full re-review each round. Added delta reviews. |
| 17 | #17 stats | feature M | 2/2 | 5 | 4 | $6.36 | 0 | Delta reviews used; round 2 caught a real double count. Reviewer over-escalated 'done twice' to needs_human; raised the bar. |
| 18 | #18 due times | feature L | 1/1 | 4 | 3 | $6.42 | 0 | Clean migration, filters/export carry time. Reviewer rated a silent wrong-day bug minor and an incomplete range fix minor; orchestrator asked about minors at handover twice. Fixed all three rules. |
| 19 | #19 HTTP API | feature L | 2/2* | 3 then 5 | 4 | $9.73 | 0 | *path /done not /close (ticket did not say). Good security (host check, local bind). Missed: make_server crashed from a thread; implementer added a test-only flag, reviewer missed it. Human review fixed it; reviewers then mutation-tested the lock. Added use-it-like-the-caller rule. Handover listed follow-ups without asking. |
| 20 | #20 rename project | feature S | 2/2 | 5 | 5 | $2.29 | 0 | No questions. Round 1 reviewer used it like a caller and found renamed names with spaces break quick add. |

# tasker eval: clean pass (2026-10-21)

All 20 issues on one frozen version of the plugin (prompts at `3a78d4e`), in a fresh repo. Questions were answered from `answers.md`, and PRs were held to the same human-review bar as the first pass. "Human saves" counts PRs where a human review comment had to fix a problem the factory missed.

| Run | Issue | Hidden | Human saves | Questions | Rounds | Cost | Denials | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | next monday | 3/3 | 0 | 0 | 1 | $1.26 | 0 | Triage in body, PR body short and clear. |
| 2 | hyphen labels | 2/2 | 0 | 1 | 1 | $1.78 | 0 | Found #5 dup, but stopped though #2 is the original (fix later). One PR closes both. |
| 3 | filter precedence | 1/1 | 0 | 0 | 1 | $1.23 | 0 | Clean. |
| 4 | monthly 31st | 1/1 | 0 | 0 | 1 | $1.25 | 0 | Chose clamp+drift itself, listed as a choice to check. |
| 5 | duplicate | n/a | 0 | 0 | 0 | $0.50 | 0 | Saw #5 already closed by #22, checked main, touched nothing. |
| 6 | search | 1/1 | 0 | 0 | 1 | $1.26 | 0 | Clean, README updated, one-word limit flagged as a choice. |
| 7 | question | n/a | 0 | 0 | 0 | $0.52 | 0 | Correct answer, linked #8 this time, no side effects. |
| 8 | every weekday | 2/2 | 0 | 0 | 1 | $1.29 | 0 | README updated this time. |
| 9 | SQL injection | 3/3 | 0 | 0 | 1 | $1.25 | 0 | Placeholder fix at the root. |
| 10 | misdescribed delete | 1/1 | 0 | 1 | 1 | $2.04 | 0 | Corrected the report, one real data-loss question, decisions written into the issue body. |
| 11 | N days filter | 2/2 | 0 | 0 | 1 | $1.24 | 0 | No questions (pass 1 asked 7). |
| 12 | vague perf | 2/2 | 0 | 0 | 1 | $1.34 | 1 | Found N+1, plain fix this time (pass 1 needed a human save). sed -i denied, fell back to Edit. |
| 13 | export/import | 2/2 | 0 | 0 | 3 | $4.00 | 0 | Chose safe refuse itself. Rounds found real bugs (orphan export crash, nested transactions). |
| 14 | undo | 3/3 | 0 | 0 | 2 | $2.55 | 0 | Round 2 caught done-twice logging a second undo entry. |
| 15 | list --json | 2/2 | 0 | 0 | 2 | $2.04 | 0 | Round 2 for orphaned-project edge case. |
| 16 | subtasks | 3/3 | 0 | 2 (spec yes, 6 spec Qs) | 1 | $7.46 | 0 | First real spec path: interview, draft PR, approval, build on same PR. Review passed round 1. |
| 17 | stats | 2/2 | 0 | 0 | 2 | $2.62 | 0 | No over-escalation this time. |
| 18 | due times | 1/1 | 1 | 0 | 3 | $8.54 | 0 | HUMAN SAVE: wrong-day save on impossible date and split time ranges; reviewer never probed them. Fix was thorough but the revision cost $5.68. |
| 19 | HTTP API | 2/2 | 0 | 0 | 1 | $2.72 | 0 | make_server works with a plain Store from a thread, no test-only flag (pass 1 needed a human save). |
| 20 | rename project | 2/2 | 0 | 0 | 2 | $2.33 | 1 | Round 2 rejected names quick add cannot read. |

## Compared with the first pass

| | First pass (prompts changing) | Clean pass (frozen) |
|---|---|---|
| Hidden tests on final main | 18/18 | 18/18 |
| Human saves | 2 (#12, #19) | 1 (#18) |
| Stops to ask the user | 10 | 3, plus a spec interview on #16 |
| Permission denials | 18 | 2 |
| Total cost | $60.48 | $47.22 |
| S and M issues | $1.08 to $3.98 | $0.50 to $4.00 |
| L issues | $6.42 to $9.73 | $2.72 to $8.54 |

## Open problems found in the clean pass

1. Triage stops on a duplicate even when the ticket being worked is the original (#2 vs #5).
2. The reviewer did not try obvious bad inputs on a parsing change (#18): impossible dates and spaced time ranges.
3. A revision after human review is expensive ($5.68 on #18), because the resumed implementer and a fresh reviewer re-read a large context.
