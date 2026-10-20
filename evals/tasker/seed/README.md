# tasker

A small Todoist-style task manager for the terminal.

```
python3 -m tasker.cli add "Buy milk tomorrow p1 #Shopping @errands"
python3 -m tasker.cli list --filter "today | overdue"
python3 -m tasker.cli done 1
```

Quick add understands priorities (`p1` to `p4`), projects (`#Work`), labels (`@home`), due dates (`today`, `tomorrow`, `friday`, `next monday`, `in 3 days`, `mar 10`, `2026-03-10`) and recurrence (`every day`, `every week`, `every month`, `every 2 weeks`, `every friday`).

Filters support `today`, `overdue`, `no date`, `p1` to `p4`, `#Project`, `@label`, `!`, `&`, `|` and parentheses.
