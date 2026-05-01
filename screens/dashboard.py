from datetime import date

from kivy.clock import Clock

from screens.base import BaseScreen


class DashboardScreen(BaseScreen):
    _seconds = 0
    _timer_event = None

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        app = self.app

        today = str(date.today())
        tasks_today = [task for task in app.state.tasks if task.get("due_date") == today]
        tasks = tasks_today or sorted(app.state.tasks, key=lambda task: task.get("due_date", ""))
        self.ids.schedule_box.text = "\n\n".join(
            task.get("title", "Task") for task in tasks[:3]
        ) if tasks else "No tasks yet"

        spent = sum(float(t.get("amount", 0)) for t in app.state.transactions)
        remaining = max(app.state.budget_limit - spent, 0)
        self.ids.budget_text.text = f"${remaining:.2f}"
        self.ids.budget_ratio.text = f"${spent:.2f}/${app.state.budget_limit:.0f}"
        self.ids.budget_progress.value = 0 if app.state.budget_limit <= 0 else min(100, (spent / app.state.budget_limit) * 100)

        self.ids.events_list.text = "\n\n".join(
            event.get("title", "Event") for event in app.state.events[:3]
        ) if app.state.events else "No events yet"
        self._render_timer()

    def _tick(self, dt):
        self._seconds += 1
        self._render_timer()

    def _render_timer(self):
        m, s = divmod(self._seconds, 60)
        self.ids.timer_label.text = f"{m}:{s:02d}"

    def play_timer(self):
        if not self._timer_event:
            self._timer_event = Clock.schedule_interval(self._tick, 1)

    def pause_timer(self):
        if self._timer_event:
            self._timer_event.cancel()
            self._timer_event = None

    def stop_timer(self):
        self.pause_timer()
        self._seconds = 0
        self._render_timer()
