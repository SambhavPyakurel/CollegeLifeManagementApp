from datetime import date, timedelta
from screens.base import BaseScreen


class RoutineAddScreen(BaseScreen):
    def confirm(self):
        title = self.ids.task_title.text.strip() or "New Task"
        category = (
            "Class" if self.ids.cat_class.active else
            "Study" if self.ids.cat_study.active else
            "Work" if self.ids.cat_work.active else
            "Other"
        )
        day = self.app.state.settings.get("routine_selected_day", "Wed")
        idx_map = {"Sun": 0, "Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5, "Sat": 6}
        target = (idx_map.get(day, 3) - 1) % 7
        today = date.today()
        delta = (target - today.weekday()) % 7
        due = today + timedelta(days=delta)
        self.app.state.tasks.append({"title": title, "category": category, "due_date": str(due), "done": False})
        self.app.persist()
        self.go("routine")

    def cancel(self):
        self.go("routine")
