import re
from datetime import date, timedelta

WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

# Due phrases that quick add looks for inside a task's text.
DUE_PATTERN = re.compile(
    r"\b(today|tomorrow|(?:next\s+)?(?:" + "|".join(WEEKDAYS) + r")"
    r"|in\s+\d+\s+(?:days?|weeks?)|\d{4}-\d{2}-\d{2}"
    r"|(?:" + "|".join(MONTHS) + r")\s+\d{1,2})\b",
    re.IGNORECASE,
)


def next_weekday(today: date, weekday: int) -> date:
    """Return the next date on or after today that falls on weekday (0 is Monday)."""
    return today + timedelta(days=(weekday - today.weekday()) % 7)


def parse_due(text: str, today: date) -> date | None:
    """Parse a due date phrase such as "tomorrow" or "next friday".

    >>> parse_due("tomorrow", date(2026, 3, 2))
    datetime.date(2026, 3, 3)
    >>> parse_due("in 2 weeks", date(2026, 3, 2))
    datetime.date(2026, 3, 16)
    """
    phrase = text.strip().lower()
    if phrase == "today":
        return today
    if phrase == "tomorrow":
        return today + timedelta(days=1)
    match = re.fullmatch(r"(next\s+)?(" + "|".join(WEEKDAYS) + ")", phrase)
    if match:
        return next_weekday(today, WEEKDAYS.index(match.group(2)))
    match = re.fullmatch(r"in\s+(\d+)\s+(day|days|week|weeks)", phrase)
    if match:
        amount = int(match.group(1))
        days = amount * 7 if match.group(2).startswith("week") else amount
        return today + timedelta(days=days)
    match = re.fullmatch(r"(" + "|".join(MONTHS) + r")\s+(\d{1,2})", phrase)
    if match:
        candidate = date(today.year, MONTHS.index(match.group(1)) + 1, int(match.group(2)))
        return candidate if candidate >= today else candidate.replace(year=today.year + 1)
    try:
        return date.fromisoformat(phrase)
    except ValueError:
        return None
