import argparse
import os
import sys
from datetime import date

from tasker import quickadd
from tasker.filters import FilterError, compile_filter
from tasker.models import Task
from tasker.recurrence import next_due
from tasker.store import INBOX, Store


def today() -> date:
    """Today's date. Tests set TASKER_TODAY to a fixed ISO date."""
    override = os.environ.get("TASKER_TODAY")
    return date.fromisoformat(override) if override else date.today()


def open_store() -> Store:
    return Store(os.environ.get("TASKER_DB", os.path.expanduser("~/.tasker.db")))


def format_task(task: Task, project_names: dict[int, str]) -> str:
    parts = [f"{task.id:>4}", f"[p{task.priority}]", task.content]
    if task.due:
        parts.append(task.due.isoformat())
    if task.recurrence:
        parts.append(f"({task.recurrence})")
    parts.append(f"#{project_names.get(task.project_id, '?')}")
    parts.extend(f"@{label}" for label in task.labels)
    return "  ".join(parts)


def cmd_add(store: Store, args: argparse.Namespace) -> int:
    parsed = quickadd.parse(" ".join(args.text), today())
    if not parsed.content:
        print("error: task has no content", file=sys.stderr)
        return 1
    project = store.get_or_create_project(parsed.project or INBOX)
    task = store.add_task(
        Task(
            id=None,
            content=parsed.content,
            project_id=project.id,
            priority=parsed.priority,
            due=parsed.due,
            labels=parsed.labels,
            recurrence=parsed.recurrence,
        )
    )
    print(f"Added task {task.id}: {task.content}")
    return 0


def cmd_list(store: Store, args: argparse.Namespace) -> int:
    project_names = {p.id: p.name for p in store.list_projects()}
    tasks = store.list_tasks()
    if args.project:
        project = store.get_project_by_name(args.project)
        if project is None:
            print(f"error: no project named {args.project}", file=sys.stderr)
            return 1
        tasks = [t for t in tasks if t.project_id == project.id]
    if args.filter:
        try:
            predicate = compile_filter(args.filter, today(), project_names)
        except FilterError as error:
            print(f"error: {error}", file=sys.stderr)
            return 1
        tasks = [t for t in tasks if predicate(t)]
    tasks.sort(key=lambda t: (t.priority, t.due or date.max, t.id))
    for task in tasks:
        print(format_task(task, project_names))
    return 0


def cmd_done(store: Store, args: argparse.Namespace) -> int:
    task = store.get_task(args.id)
    if task is None:
        print(f"error: no task {args.id}", file=sys.stderr)
        return 1
    if task.recurrence and task.due:
        task.due = next_due(task.recurrence, task.due)
        store.update_task(task)
        print(f"Task {task.id} is next due {task.due.isoformat()}")
        return 0
    task.completed = True
    store.update_task(task)
    print(f"Completed task {task.id}: {task.content}")
    return 0


def cmd_projects(store: Store, args: argparse.Namespace) -> int:
    for project in store.list_projects():
        print(project.name)
    return 0


def cmd_delete_project(store: Store, args: argparse.Namespace) -> int:
    project = store.get_project_by_name(args.name)
    if project is None:
        print(f"error: no project named {args.name}", file=sys.stderr)
        return 1
    if project.name == INBOX:
        print("error: the Inbox cannot be deleted", file=sys.stderr)
        return 1
    store.delete_project(project.id)
    print(f"Deleted project {project.name}")
    return 0


def cmd_label(store: Store, args: argparse.Namespace) -> int:
    project_names = {p.id: p.name for p in store.list_projects()}
    for task in store.tasks_with_label(args.label):
        print(format_task(task, project_names))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tasker", description="A small task manager.")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Add a task with quick add syntax")
    add.add_argument("text", nargs="+")
    add.set_defaults(func=cmd_add)

    list_ = sub.add_parser("list", help="List open tasks")
    list_.add_argument("--filter", help='Filter query, for example "today & p1"')
    list_.add_argument("--project", help="Only tasks in this project")
    list_.set_defaults(func=cmd_list)

    done = sub.add_parser("done", help="Complete a task")
    done.add_argument("id", type=int)
    done.set_defaults(func=cmd_done)

    projects = sub.add_parser("projects", help="List projects")
    projects.set_defaults(func=cmd_projects)

    delete_project = sub.add_parser("delete-project", help="Delete a project")
    delete_project.add_argument("name")
    delete_project.set_defaults(func=cmd_delete_project)

    label = sub.add_parser("label", help="List open tasks with a label")
    label.add_argument("label")
    label.set_defaults(func=cmd_label)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    store = open_store()
    return args.func(store, args)


if __name__ == "__main__":
    raise SystemExit(main())
