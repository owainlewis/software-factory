# Product owner answers

Use these for questions from either arm, so both get the same answers.

- 1: Any layout is fine. CI on pull requests and pushes to main.
- 2: Validation errors are 422 (FastAPI's default). Email comparison for uniqueness ignores case.
- 3: `total` is the count before limit and offset. Unknown `sort` is 422.
- 4: Deleting a company: see #5. Domain is stored lower case.
- 5: A missing `company_id` on create or update is 422.
- 6: Domain match ignores case. Only on create, not on update. Subdomains do not match.
- 7: `value` is a non-negative integer. Unknown stage is 422. Deleting a company or contact keeps the deal with the link cleared.
- 8: `closed_at` is set when a deal moves to won or lost. While a deal is closed, changing anything except `stage` is 409. Moving it back to an open stage reopens it and clears `closed_at`.
- 9: Values are summed across currencies as plain numbers. Fine for now.
- 10: An activity with none of the three ids, or with an id that does not exist, is 422.
- 11: Activities on the contact's company are not included. Each activity appears once.
- 12: Each list is capped at 20. Empty `q` is 422.
- 13: Tags are lower case, letters, digits and hyphens. Duplicate tags are removed.
- 14: If it already works, say so and change nothing.
- 15: All text is HTML-escaped.
- 17: After a successful create, redirect with 303.
- 18: Tokens do not expire. Duplicate email on register is 409. Wrong password on login is 401.
- 19: Deals created before accounts existed have no owner. `owner=me` without auth is 401.
- 20: A session cookie after a form post to `/login` with `email` and `password`. Users register through the API. Add `/logout`.
- 21: Header names must match. A row with a bad email goes in `errors`. Max 5 MB.
- 22: Columns in the order `first_name,last_name,email,company`.
- 23: `won_value_this_month` uses `closed_at`.
- 24: Deleting a contact keeps their deals and activities. Their links to the contact are cleared.
- 25: Signed-out visitors go to `/login`.
- Anything else: choose the simplest behavior a typical CRM has, and say so in the PR.
