import re
from datetime import date, timedelta

from tasker.dates import WEEKDAYS, next_weekday

RECURRENCE_PATTERN = re.compile(
    r"\bevery\s+(?:day|week|month|\d+\s+(?:days|weeks)|" + "|".join(WEEKDAYS) + r")\b",
    re.IGNORECASE,
)


def next_due(rule: str, current: date) -> date:
    """Return the next due date for a recurrence rule such as "every week".

    >>> next_due("every week", date(2026, 3, 2))
    datetime.date(2026, 3, 9)
    """
    rule = rule.strip().lower()
    if rule == "every day":
        return current + timedelta(days=1)
    if rule == "every week":
        return current + timedelta(weeks=1)
    if rule == "every month":
        if current.month == 12:
            return current.replace(year=current.year + 1, month=1)
        return current.replace(month=current.month + 1)
    match = re.fullmatch(r"every\s+(\d+)\s+(days|weeks)", rule)
    if match:
        amount = int(match.group(1))
        return current + timedelta(days=amount * 7 if match.group(2) == "weeks" else amount)
    match = re.fullmatch(r"every\s+(" + "|".join(WEEKDAYS) + ")", rule)
    if match:
        return next_weekday(current + timedelta(days=1), WEEKDAYS.index(match.group(1)))
    raise ValueError(f"unknown recurrence: {rule}")
