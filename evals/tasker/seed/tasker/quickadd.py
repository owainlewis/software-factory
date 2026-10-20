import re
from dataclasses import dataclass, field
from datetime import date

from tasker.dates import DUE_PATTERN, parse_due
from tasker.recurrence import RECURRENCE_PATTERN, next_due


@dataclass
class QuickAdd:
    content: str
    priority: int = 4
    due: date | None = None
    project: str | None = None
    labels: list[str] = field(default_factory=list)
    recurrence: str | None = None


def parse(text: str, today: date) -> QuickAdd:
    """Parse Todoist-style quick add text.

    >>> q = parse("Buy milk tomorrow p1 #Shopping @errands", date(2026, 3, 2))
    >>> (q.content, q.priority, q.due, q.project, q.labels)
    ('Buy milk', 1, datetime.date(2026, 3, 3), 'Shopping', ['errands'])
    """
    result = QuickAdd(content="")
    rest = text

    labels = re.findall(r"@(\w+)", rest)
    result.labels = sorted(set(labels))
    rest = re.sub(r"@\w+", "", rest)

    project = re.search(r"#(\S+)", rest)
    if project:
        result.project = project.group(1)
        rest = rest.replace(project.group(0), "")

    priority = re.search(r"\bp([1-4])\b", rest)
    if priority:
        result.priority = int(priority.group(1))
        rest = rest.replace(priority.group(0), "", 1)

    recurrence = RECURRENCE_PATTERN.search(rest)
    if recurrence:
        result.recurrence = recurrence.group(0).lower()
        rest = rest.replace(recurrence.group(0), "", 1)

    due = DUE_PATTERN.search(rest)
    if due:
        result.due = parse_due(due.group(0), today)
        rest = rest.replace(due.group(0), "", 1)
    elif result.recurrence:
        result.due = today if result.recurrence == "every day" else next_due(result.recurrence, today)

    result.content = " ".join(rest.split())
    return result
