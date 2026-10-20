from dataclasses import dataclass, field
from datetime import date


@dataclass
class Project:
    id: int | None
    name: str


@dataclass
class Task:
    id: int | None
    content: str
    project_id: int
    priority: int = 4  # 1 is the highest priority, 4 is the default
    due: date | None = None
    labels: list[str] = field(default_factory=list)
    recurrence: str | None = None
    completed: bool = False
