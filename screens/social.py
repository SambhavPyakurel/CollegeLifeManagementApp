from screens.base import BaseScreen


class SocialScreen(BaseScreen):
    selected_category = "all"

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self._sync_filter_checks()
        self.apply_filter(self.selected_category)

    def apply_filter(self, category):
        if category != "all":
            all_box = self.ids.get("filter_all")
            if all_box:
                all_box.active = False
        self.selected_category = category
        if category == "all":
            for name in ("filter_sports", "filter_academic", "filter_life"):
                checkbox = self.ids.get(name)
                if checkbox:
                    checkbox.active = False
        events = self.app.state.events
        if category != "all":
            events = [event for event in events if event.get("category") == category]

        box = self.ids.event_list_box
        box.clear_widgets()
        from kivy.uix.button import Button
        from kivy.uix.widget import Widget
        for ev in events:
            btn = Button(
                text=ev["title"],
                size_hint_y=None,
                height=62,
                background_normal="",
                background_color=(0.16, 0.27, 0.28, 1) if self.app.state.settings.get("dark_mode") else (0.93, 1.0, 1.0, 1),
                color=self.app.text_color,
                bold=True,
                font_size="22sp",
            )
            btn.bind(on_release=lambda _, event_id=ev["id"]: self.open_desc(event_id))
            box.add_widget(btn)
        if not events:
            from kivy.uix.label import Label
            box.add_widget(Label(
                text="No events in this category",
                size_hint_y=None,
                height=80,
                color=self.app.muted_text_color,
                font_size="18sp",
            ))
        elif len(events) < 3:
            for _ in range(3 - len(events)):
                box.add_widget(Widget(size_hint_y=None, height=10))
        self._apply_font_scale(box)
        self._apply_theme_colors(box)

    def open_create(self):
        self.go("social_add")

    def open_desc(self, event_id):
        self.app.state.settings["selected_event_id"] = event_id
        self.go("social_desc")

    def apply_checked_filters(self):
        selected = [
            ("sports", self.ids.filter_sports.active),
            ("academic", self.ids.filter_academic.active),
            ("stud_life", self.ids.filter_life.active),
        ]
        checked = [category for category, active in selected if active]
        if not checked:
            self.selected_category = "all"
            self.ids.filter_all.active = True
            self.apply_filter("all")
        else:
            self.ids.filter_all.active = False
            self.apply_filter(checked[-1])

    def show_all(self):
        self.selected_category = "all"
        self._sync_filter_checks()
        self.apply_filter("all")

    def _sync_filter_checks(self):
        if "filter_all" not in self.ids:
            return
        self.ids.filter_all.active = self.selected_category == "all"
        self.ids.filter_sports.active = self.selected_category == "sports"
        self.ids.filter_academic.active = self.selected_category == "academic"
        self.ids.filter_life.active = self.selected_category == "stud_life"
