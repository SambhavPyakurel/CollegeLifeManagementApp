from datetime import date

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label

from screens.base import BaseScreen


class RoutineScreen(BaseScreen):
    selected_day = "Wed"
    _day_index = {"Sun": 0, "Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5, "Sat": 6}
    _category_icons = {
        "Class": "assets/blue.png",
        "Study": "assets/red.png",
        "Work": "assets/yellow.png",
        "Other": "assets/green.png",
    }
    _boilerplate = {
        ("Task 1", "Study"),
        ("Task 2", "Class"),
        ("Task 3", "Work"),
    }

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self._remove_boilerplate_tasks()
        self._refresh_day_header()
        self.refresh_tasks()

    def _remove_boilerplate_tasks(self):
        before = len(self.app.state.tasks)
        self.app.state.tasks = [
            task for task in self.app.state.tasks
            if (task.get("title"), task.get("category")) not in self._boilerplate
        ]
        if len(self.app.state.tasks) != before:
            self.app.persist()

    def select_day(self, day):
        self.selected_day = day
        self._refresh_day_header()
        self.refresh_tasks()

    def _refresh_day_header(self):
        self.ids.day_title.text = f"{self.selected_day}'s Schedule"
        for day in self._day_index:
            btn = self.ids.get(f"day_{day}")
            if btn:
                btn.background_color = (0.20, 0.20, 0.20, 1) if day == self.selected_day else (0, 0, 0, 0)
                btn.color = (1, 1, 1, 1) if day == self.selected_day else self.app.text_color

    def refresh_tasks(self):
        target_weekday = (self._day_index.get(self.selected_day, 3) - 1) % 7
        tasks = [
            task for task in self.app.state.tasks
            if date.fromisoformat(task["due_date"]).weekday() == target_weekday
        ]
        self._shown = tasks

        box = self.ids.task_list_box
        box.clear_widgets()

        if not tasks:
            box.add_widget(Label(
                text="No tasks yet",
                size_hint_y=None,
                height=80,
                color=self.app.muted_text_color,
                font_size="20sp",
                halign="center",
                valign="middle",
            ))
            self._apply_font_scale(box)
            return

        for index, task in enumerate(tasks):
            category = task.get("category", "Other")
            row = BoxLayout(
                size_hint_y=None,
                height=62,
                padding=[16, 8, 16, 8],
                spacing=14,
            )
            with row.canvas.before:
                from kivy.graphics import Color, RoundedRectangle
                Color(*( [0.16, 0.27, 0.28, 1] if self.app.state.settings.get("dark_mode") else [0.88, 1.0, 1.0, 1] ))
                row._bg = RoundedRectangle(pos=row.pos, size=row.size, radius=[30])
            row.bind(pos=lambda widget, *_: setattr(widget._bg, "pos", widget.pos))
            row.bind(size=lambda widget, *_: setattr(widget._bg, "size", widget.size))

            row.add_widget(Image(
                source=self._category_icons.get(category, self._category_icons["Other"]),
                size_hint_x=None,
                width=34,
                fit_mode="contain",
            ))
            title = Label(
                text=task.get("title", "Task"),
                color=self.app.text_color,
                bold=True,
                font_size="22sp",
                halign="left",
                valign="middle",
            )
            title.bind(size=lambda label, *_: setattr(label, "text_size", label.size))
            row.add_widget(title)
            delete = Button(
                size_hint_x=None,
                width=42,
                background_normal="assets/bin.png",
                background_down="assets/bin.png",
                background_color=(1, 1, 1, 1),
                border=(0, 0, 0, 0),
            )
            delete.bind(on_release=lambda _, slot=index: self.delete_task(slot))
            row.add_widget(delete)
            box.add_widget(row)
        self._apply_font_scale(box)
        self._apply_theme_colors(box)

    def delete_task(self, slot):
        if slot >= len(self._shown):
            return
        target = self._shown[slot]
        self.app.state.tasks = [task for task in self.app.state.tasks if task is not target]
        self.app.persist()
        self.refresh_tasks()

    def open_add(self):
        self.app.state.settings["routine_selected_day"] = self.selected_day
        self.go("routine_add")
