from __future__ import annotations

import json
import sys
from pathlib import Path


class TaskStore:
    PRIORITY_ORDER = {"high": 1, "medium": 2, "low": 3}
    PRIORITY_LABELS = {"high": "High", "medium": "Medium", "low": "Low"}

    def __init__(self, storage_path: Path | None = None):
        self.storage_path = Path(storage_path) if storage_path is not None else self.resolve_storage_path()
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            self.storage_path.write_text("[]", encoding="utf-8")
        self.tasks = self.load_tasks()

    @staticmethod
    def resolve_storage_path() -> Path:
        if getattr(sys, "_MEIPASS", None):
            return Path.home() / ".ssquad" / "tasks.json"
        return Path(__file__).resolve().parent / "tasks.json"

    def load_tasks(self):
        try:
            raw_data = json.loads(self.storage_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            raw_data = []

        tasks = []
        for task in raw_data:
            if not isinstance(task, dict):
                continue

            title = str(task.get("title", "")).strip()
            if not title:
                continue

            tasks.append(
                {
                    "id": int(task.get("id", 0) or 0),
                    "title": title,
                    "description": str(task.get("description", "")).strip(),
                    "priority": self.normalize_priority(task.get("priority")),
                    "due_date": str(task.get("due_date", "")).strip(),
                    "completed": bool(task.get("completed", False)),
                }
            )

        tasks.sort(key=lambda item: item["id"])
        return tasks

    @classmethod
    def normalize_priority(cls, value) -> str:
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in cls.PRIORITY_ORDER:
                return normalized
            if normalized.isdigit() and int(normalized) in cls.PRIORITY_ORDER.values():
                return next(key for key, rank in cls.PRIORITY_ORDER.items() if rank == int(normalized))

        if isinstance(value, int):
            if value in cls.PRIORITY_ORDER.values():
                return next(key for key, rank in cls.PRIORITY_ORDER.items() if rank == value)

        return "medium"

    def save_tasks(self):
        self.storage_path.write_text(json.dumps(self.tasks, indent=2), encoding="utf-8")

    def get_tasks(self):
        return [dict(task) for task in self.tasks]

    def next_id(self):
        if not self.tasks:
            return 1
        return max(task["id"] for task in self.tasks) + 1

    def add_task(self, title, description, priority, due_date):
        task = {
            "id": self.next_id(),
            "title": title,
            "description": description,
            "priority": self.normalize_priority(priority),
            "due_date": due_date,
            "completed": False,
        }
        self.tasks.append(task)
        self.save_tasks()
        return dict(task)

    def update_task(self, task_id, **changes):
        for task in self.tasks:
            if task["id"] == task_id:
                for key, value in changes.items():
                    if key == "priority":
                        task[key] = self.normalize_priority(value)
                    elif key == "completed":
                        task[key] = bool(value)
                    else:
                        task[key] = value
                self.save_tasks()
                return dict(task)
        return None

    def toggle_complete(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                self.save_tasks()
                return dict(task)
        return None

    def delete_task(self, task_id):
        original_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        if len(self.tasks) != original_count:
            self.save_tasks()
            return True
        return False
