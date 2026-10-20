# Product owner answers (for relayed questions)

- 1: "next X" = the X in the following 7 days but never today; on Monday "next monday" is +7. Plain weekday on that weekday = today.
- 4: clamp to the last day of the month (Jan 31 -> Feb 28 -> Mar 28 is fine).
- 8: first due date when added on a weekend = next Monday; on a weekday = today.
- 10: deleting a project deletes its tasks too, like Todoist. Print how many tasks were deleted. Inbox cannot be deleted.
- 11: `N days` = today <= due <= today + N. Overdue tasks are not included.
- 13: JSON shape is up to you. Import into a non-empty database: refuse with an error.
- 14: one level of undo is enough. Undo of a recurring task restores the old due date. Undo with nothing to undo: print a message and exit 1.
- 15: due as ISO string or null, project as name.
- 16: one level of nesting only. Completing a parent completes its subtasks. Filters apply to each task on its own; a subtask shown without its parent is shown unindented. --parent must refer to an open task.
- 17: completion time stored when a task is done (recurring completions count too).
- 18: times like 5pm, 5:30pm, 17:00. "today" filter matches timed tasks due today. Sorting: untimed tasks after timed ones on the same day.
- 19: GET /tasks, POST /tasks {"text": "..."}, POST /tasks/<id>/done. JSON responses. 404 for unknown task.
- 20: error (exit 1) if OLD does not exist or NEW already exists. Inbox cannot be renamed. Case-only rename (work -> Work) is allowed.
- Anything else: pick the most Todoist-like behavior and record it as an assumption.
