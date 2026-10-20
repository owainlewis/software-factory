import sqlite3
from datetime import date

from tasker.models import Project, Task

INBOX = "Inbox"

MIGRATIONS = [
    """
    CREATE TABLE projects (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    );
    CREATE TABLE tasks (
        id INTEGER PRIMARY KEY,
        content TEXT NOT NULL,
        project_id INTEGER NOT NULL REFERENCES projects(id),
        priority INTEGER NOT NULL DEFAULT 4,
        due TEXT,
        recurrence TEXT,
        completed INTEGER NOT NULL DEFAULT 0
    );
    CREATE TABLE task_labels (
        task_id INTEGER NOT NULL REFERENCES tasks(id),
        label TEXT NOT NULL,
        PRIMARY KEY (task_id, label)
    );
    """,
]


class Store:
    """SQLite storage for projects and tasks."""

    def __init__(self, path: str = ":memory:") -> None:
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self._migrate()
        if self.get_project_by_name(INBOX) is None:
            self.add_project(INBOX)

    def _migrate(self) -> None:
        self.conn.execute("CREATE TABLE IF NOT EXISTS schema_version (version INTEGER NOT NULL)")
        row = self.conn.execute("SELECT version FROM schema_version").fetchone()
        current = row["version"] if row else 0
        for version, sql in enumerate(MIGRATIONS[current:], start=current + 1):
            self.conn.executescript(sql)
            self.conn.execute("DELETE FROM schema_version")
            self.conn.execute("INSERT INTO schema_version (version) VALUES (?)", (version,))
        self.conn.commit()

    # Projects

    def add_project(self, name: str) -> Project:
        cur = self.conn.execute("INSERT INTO projects (name) VALUES (?)", (name,))
        self.conn.commit()
        return Project(cur.lastrowid, name)

    def get_project(self, project_id: int) -> Project | None:
        row = self.conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
        return Project(row["id"], row["name"]) if row else None

    def get_project_by_name(self, name: str) -> Project | None:
        row = self.conn.execute(
            "SELECT * FROM projects WHERE name = ? COLLATE NOCASE", (name,)
        ).fetchone()
        return Project(row["id"], row["name"]) if row else None

    def get_or_create_project(self, name: str) -> Project:
        return self.get_project_by_name(name) or self.add_project(name)

    def list_projects(self) -> list[Project]:
        rows = self.conn.execute("SELECT * FROM projects ORDER BY id").fetchall()
        return [Project(r["id"], r["name"]) for r in rows]

    def delete_project(self, project_id: int) -> None:
        self.conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        self.conn.commit()

    # Tasks

    def add_task(self, task: Task) -> Task:
        cur = self.conn.execute(
            "INSERT INTO tasks (content, project_id, priority, due, recurrence, completed)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (
                task.content,
                task.project_id,
                task.priority,
                task.due.isoformat() if task.due else None,
                task.recurrence,
                int(task.completed),
            ),
        )
        task.id = cur.lastrowid
        self._save_labels(task)
        self.conn.commit()
        return task

    def update_task(self, task: Task) -> None:
        self.conn.execute(
            "UPDATE tasks SET content = ?, project_id = ?, priority = ?, due = ?,"
            " recurrence = ?, completed = ? WHERE id = ?",
            (
                task.content,
                task.project_id,
                task.priority,
                task.due.isoformat() if task.due else None,
                task.recurrence,
                int(task.completed),
                task.id,
            ),
        )
        self._save_labels(task)
        self.conn.commit()

    def _save_labels(self, task: Task) -> None:
        self.conn.execute("DELETE FROM task_labels WHERE task_id = ?", (task.id,))
        self.conn.executemany(
            "INSERT INTO task_labels (task_id, label) VALUES (?, ?)",
            [(task.id, label) for label in task.labels],
        )

    def get_task(self, task_id: int) -> Task | None:
        row = self.conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        return self._row_to_task(row) if row else None

    def list_tasks(self, include_completed: bool = False) -> list[Task]:
        sql = "SELECT * FROM tasks"
        if not include_completed:
            sql += " WHERE completed = 0"
        sql += " ORDER BY id"
        return [self._row_to_task(r) for r in self.conn.execute(sql).fetchall()]

    def tasks_with_label(self, label: str) -> list[Task]:
        rows = self.conn.execute(
            "SELECT t.* FROM tasks t JOIN task_labels l ON l.task_id = t.id"
            f" WHERE l.label = '{label}' AND t.completed = 0 ORDER BY t.id"
        ).fetchall()
        return [self._row_to_task(r) for r in rows]

    def list_labels(self) -> list[str]:
        rows = self.conn.execute("SELECT DISTINCT label FROM task_labels ORDER BY label").fetchall()
        return [r["label"] for r in rows]

    def _row_to_task(self, row: sqlite3.Row) -> Task:
        labels = [
            r["label"]
            for r in self.conn.execute(
                "SELECT label FROM task_labels WHERE task_id = ? ORDER BY label", (row["id"],)
            ).fetchall()
        ]
        return Task(
            id=row["id"],
            content=row["content"],
            project_id=row["project_id"],
            priority=row["priority"],
            due=date.fromisoformat(row["due"]) if row["due"] else None,
            labels=labels,
            recurrence=row["recurrence"],
            completed=bool(row["completed"]),
        )
