# CRM from scratch: factory vs plain Claude Code (2026-10-21 to 22)

The same 25 tickets, from an empty repo to a working CRM (FastAPI, SQLite, web pages, accounts, CSV, dashboard), in two private repos:

- **Factory:** `/software-factory:factory <issue>`, using the plugin installed from GitHub (`76a6961`).
- **Vanilla:** `claude -p "Implement GitHub issue <url>. Read the issue, build it with tests, and open a pull request that closes it."`

Both arms used the same model, tool allowlist, product-owner answers (`answers.md`) and review bar. Hidden acceptance tests (`hidden/`) and a robustness probe (`hidden/probe_robustness.py`) were never shown to either arm.

## Result

| | Factory | Vanilla |
|---|---|---|
| Hidden tests on final main | 26/26 | 26/26 |
| PRs that failed hidden tests as delivered | 0 | 1 (#24) |
| Human saves (I had to request changes) | 0 | 1 |
| Robustness probe (16 checks, unseen) | 16/16 | 15/16 |
| Stops to ask a question | 5 | 0 |
| PRs merged by the approver | 5 of 24 | n/a |
| Total cost | $55.43 | $22.61 |
| Model time | 187 min | 59 min |
| App / test lines | 1,932 / 3,792 | 1,800 / 3,461 |
| Test suite runtime | 67 s | 20 s |

## What the factory bought

- **No human saves.** Vanilla once made a large design decision on its own: given "deleting a contact loses history", it switched to soft delete, rebuilt the contacts table and broke ticket 2's contract. The factory asked first on the same ticket.
- **Risks surfaced before merge:**
  - a dependency pinned to a day-old release (`httpx2`, checked: legitimate)
  - totals that add up mixed currencies
  - CSV formula injection on export
  - open registration
  - a password-hash cost that couldn't be raised later

  Vanilla shipped the same choices without comment.
- **Robustness:** review fixed a 500 error on huge ids on ticket 2. Vanilla's final app still has it.

## What it cost

- **2.5x the cost and 3x the time** for the same hidden-test result.
- **The approver merged only 5 of 24 PRs.** Almost every greenfield ticket adds schema or public API, so a person still merged 19.
- **No memory across tickets.** It asked about mixed currencies on #9, then again on #23.
- **Slower tests.** The test suite runs 3x slower: it hashes passwords for real in tests, where vanilla used cheap test settings.

## Harness fixes during the run (applied to both arms)

- Hidden tests now run app startup hooks (`with TestClient`), because both apps create tables on startup.
- The timeline test sends timestamps with a timezone, because both apps reject timestamps without one, and say so clearly.

## Per ticket

| Ticket | Arm | Hidden (cumulative) | Human save | Questions | Rounds | Merged by | Cost | Denials | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 setup | vanilla | 1/1 | 0 | 0 | - | me | $0.66 | 4 | CI added, passes. |
| 2 contacts | vanilla | 3/3 | 0 | 0 | - | me | $0.62 | 2 | Tables made in startup hook (fixed my harness, not a defect). |
| 1 setup | factory | 1/1 | 0 | 0 | 1 | me (escalated) | $1.52 | 3 | Escalated: new deps, lock, CI. Flagged httpx2 pinned to a day-old release (checked: legit). |
| 3 pagination | vanilla | 4/4 | 0 | 0 | - | me | $0.69 | 1 | |
| 4 companies | vanilla | 5/5 | 0 | 0 | - | me | $0.65 | 1 | |
| 5 link companies | vanilla | 6/6 | 0 | 0 | - | me | $0.84 | 1 | |
| 6 domain link | vanilla | 7/7 | 0 | 0 | - | me | $0.49 | 0 | |
| 2 contacts | factory | 3/3 | 0 | 0 | 2 | me (escalated) | $2.35 | 1 | Review fixed case-insensitive duplicate emails and 500 on huge ids. |
| 7 deals | vanilla | 8/8 | 0 | 0 | - | me | $0.74 | 0 | |
| 8 closed deals | vanilla | 9/9 | 0 | 0 | - | me | $0.80 | 1 | Vague ticket: assumed sensibly, listed its choices in the PR. |
| 9 pipeline | vanilla | 10/10 | 0 | 0 | - | me | $0.59 | 1 | |
| 3 pagination | factory | 4/4 | 0 | 0 | 1 | me (escalated) | $2.00 | 2 | |
| 10 activities | vanilla | 11/11 | 0 | 0 | - | me | $0.88 | 2 | |
| 11 timeline | vanilla | 12/12 | 0 | 0 | - | me | $0.63 | 0 | Requires timezone-aware timestamps (my test fixed to send Z). |
| 4 companies | factory | 5/5 | 0 | 0 | 1 | me (escalated) | $1.78 | 1 | |
| 12 search | vanilla | 13/13 | 0 | 0 | - | me | $0.62 | 0 | |
| 13 tags | vanilla | 14/14 | 0 | 0 | - | me | $0.75 | 0 | |
| 14 trap: already works | vanilla | 15/15 | 0 | 0 | - | me | $0.52 | 1 | Saw it already works; added a regression test only. |
| 5 link companies | factory | 6/6 | 0 | 0 | 1 | me (escalated) | $2.23 | 1 | |
| 15 contact pages | vanilla | 16/16 | 0 | 0 | - | me | $1.02 | 3 | HTML escaped. |
| 16 deals board | vanilla | 17/17 | 0 | 0 | - | me | $0.68 | 1 | |
| 6 domain link | factory | 7/7 | 0 | 0 | 1 | me (escalated) | $1.72 | 2 | |
| 17 contact form | vanilla | 18/18 | 0 | 0 | - | me | $0.89 | 2 | |
| 18 accounts | vanilla | 19/19 | 0 | 0 | - | me | $1.07 | 1 | scrypt, hashed tokens, a 401 test per endpoint. |
| 7 deals | factory | 8/8 | 0 | 0 | 1 | me (escalated) | $1.97 | 1 | |
| 19 deal owners | vanilla | 20/20 | 0 | 0 | - | me | $0.99 | 3 | |
| 20 web sign-in | vanilla | 21/21 | 0 | 0 | - | me | $0.96 | 0 | |
| 8 closed deals | factory | 9/9 | 0 | 1 (4 Qs) | 1 | me (escalated) | $2.96 | 3 | Asked 4 good questions where vanilla guessed (and guessed right). |
| 21 CSV import | vanilla | 22/22 | 0 | 0 | - | me | $0.82 | 0 | |
| 22 CSV export | vanilla | 23/23 | 0 | 0 | - | me | $0.65 | 0 | |
| 9 pipeline | factory | 10/10 | 0 | 1 (currency) | 1 | approver (auto) | $2.42 | 1 | Asked about mixed currencies (vanilla summed silently). First auto-merge. |
| 23 dashboard numbers | vanilla | 24/24 | 0 | 0 | - | me | $0.61 | 0 | |
| 10 activities | factory | 11/11 | 0 | 0 | 1 | me (escalated) | $2.17 | 1 | |
| 24 delete keeps history | vanilla | 25/25 after save (23/25 first) | 1 | 0 | - | me | $4.69 | 2 | HUMAN SAVE: chose soft delete on its own, rebuilt the table and broke the ticket 2 contract (GET deleted = 200). The existing behaviour already met the ask; after revert the PR was tests only. |
| 25 dashboard page | vanilla | 26/26 | 0 | 0 | - | me | $0.75 | 1 | |
| 11 timeline | factory | 12/12 | 0 | 0 | 1 | approver (auto) | $1.86 | 3 | |
| 12 search | factory | 13/13 | 0 | 0 | 1 | me (escalated) | $1.88 | 0 | Linked the #14 trap as also fixed. |
| 13 tags | factory | 14/14 | 0 | 0 | 1 | me (escalated) | $2.58 | 2 | |
| 14 trap: already works | factory | 15/15 | 0 | 0 | 0 | n/a | $0.58 | 0 | Saw #14 already closed by #37, checked main, no PR. |
| 15 contact pages | factory | 16/16 | 0 | 0 | 1 | me (escalated) | $2.35 | 3 | |
| 16 deals board | factory | 17/17 | 0 | 0 | 1 | approver (auto) | $1.67 | 0 | |
| 17 contact form | factory | 18/18 | 0 | 0 | 1 | me (escalated) | $2.20 | 1 | |
| 18 accounts | factory | 19/19 | 0 | 0 | 1 | me (escalated) | $2.52 | 0 | Flagged open registration and the scrypt upgrade path. Suite slowed to 54s (no cheap test hashing). |
| 19 deal owners | factory | 20/20 | 0 | 0 | 1 | me (escalated) | $2.21 | 1 | |
| 20 web sign-in | factory | 21/21 | 0 | 1 (5 Qs) | 1 | me (escalated) | $3.55 | 1 | Good session-design questions. |
| 21 CSV import | factory | 22/22 | 0 | 0 | 2+ | me (escalated) | $3.66 | 1 | |
| 22 CSV export | factory | 23/23 | 0 | 0 | 1 | me (escalated) | $1.96 | 0 | Raised CSV formula injection with trade-offs (vanilla silent). |
| 23 dashboard numbers | factory | 24/24 | 0 | 1 (currency again) | 1 | approver (auto) | $2.84 | 0 | Re-asked the currency question already settled on #9: no memory across tickets. |
| 24 delete keeps history | factory | 25/25 | 0 | 1 (asked before building) | 1 | approver (auto) | $2.60 | 0 | Asked instead of building soft delete; test-only PR auto-merged. |
| 25 dashboard page | factory | 26/26 | 0 | 0 | 1 | me (escalated) | $1.85 | 2 | |
