import json
from pathlib import Path
from services.models import AppState

class StorageService:
    def __init__(self, path="data/app_state.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self):
        if not self.path.exists():
            return AppState()
        with self.path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        state = AppState()
        state.settings = raw.get("settings", state.settings)
        state.tasks = raw.get("tasks", state.tasks)
        boilerplate_tasks = {("Task 1", "Study"), ("Task 2", "Class"), ("Task 3", "Work")}
        state.tasks = [
            task for task in state.tasks
            if (task.get("title"), task.get("category")) not in boilerplate_tasks
        ]
        task_categories = {
            "class": "Class",
            "study": "Study",
            "work": "Work",
            "other": "Other",
        }
        for task in state.tasks:
            normalized = task_categories.get(str(task.get("category", "Other")).lower())
            task["category"] = normalized or "Other"
        state.transactions = raw.get("transactions", state.transactions)
        state.budget_limit = raw.get("budget_limit", state.budget_limit)
        state.resources = raw.get("resources", state.resources)
        state.events = raw.get("events", state.events)
        categories = ["stud_life", "academic", "sports"]
        for index, event in enumerate(state.events):
            event.setdefault("category", categories[index % len(categories)])
        return state

    def save(self, state: AppState):
        payload = {
            "settings": state.settings,
            "tasks": state.tasks,
            "transactions": state.transactions,
            "budget_limit": state.budget_limit,
            "resources": state.resources,
            "events": state.events,
        }
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def reset(self):
        self.save(AppState())

