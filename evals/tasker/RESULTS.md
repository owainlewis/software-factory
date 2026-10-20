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
