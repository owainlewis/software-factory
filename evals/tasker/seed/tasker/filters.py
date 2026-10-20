"""A small Todoist-style filter language.

Terms: today, overdue, "no date", p1 to p4, #Project, @label.
Operators: ! (not), & (and), | (or), and parentheses.
"""

import re
from collections.abc import Callable
from datetime import date

from tasker.models import Task

Predicate = Callable[[Task], bool]

TOKEN = re.compile(r"\s*(\(|\)|&|\||!|no date|[#@]\S+?(?=[\s&|)]|$)|[a-z0-9]+)", re.IGNORECASE)


class FilterError(ValueError):
    pass


def tokenize(query: str) -> list[str]:
    tokens = []
    pos = 0
    query = query.strip()
    while pos < len(query):
        match = TOKEN.match(query, pos)
        if not match:
            raise FilterError(f"cannot parse filter at: {query[pos:]!r}")
        tokens.append(match.group(1))
        pos = match.end()
    return tokens


def compile_filter(query: str, today: date, project_names: dict[int, str]) -> Predicate:
    """Turn a filter query into a predicate over tasks."""
    tokens = tokenize(query)
    pos = 0

    def term(token: str) -> Predicate:
        lowered = token.lower()
        if lowered == "today":
            return lambda t: t.due == today
        if lowered == "overdue":
            return lambda t: t.due is not None and t.due < today
        if lowered == "no date":
            return lambda t: t.due is None
        if re.fullmatch(r"p[1-4]", lowered):
            level = int(lowered[1])
            return lambda t: t.priority == level
        if token.startswith("#"):
            name = token[1:].lower()
            return lambda t: project_names.get(t.project_id, "").lower() == name
        if token.startswith("@"):
            label = token[1:].lower()
            return lambda t: label in [x.lower() for x in t.labels]
        raise FilterError(f"unknown filter term: {token}")

    def unary() -> Predicate:
        nonlocal pos
        if pos >= len(tokens):
            raise FilterError("unexpected end of filter")
        token = tokens[pos]
        pos += 1
        if token == "!":
            inner = unary()
            return lambda t: not inner(t)
        if token == "(":
            inner = expression()
            if pos >= len(tokens) or tokens[pos] != ")":
                raise FilterError("missing )")
            pos += 1
            return inner
        return term(token)

    def expression() -> Predicate:
        nonlocal pos
        left = unary()
        while pos < len(tokens) and tokens[pos] in ("&", "|"):
            op = tokens[pos]
            pos += 1
            right = unary()
            if op == "&":
                left = (lambda a, b: lambda t: a(t) and b(t))(left, right)
            else:
                left = (lambda a, b: lambda t: a(t) or b(t))(left, right)
        return left

    predicate = expression()
    if pos != len(tokens):
        raise FilterError(f"unexpected token: {tokens[pos]}")
    return predicate
