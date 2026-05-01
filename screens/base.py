from kivy.uix.screenmanager import Screen
from kivy.app import App


class BaseScreen(Screen):
    active_tab = "dashboard"

    @property
    def app(self):
        return App.get_running_app()

    def go(self, screen_name):
        self.manager.current = screen_name

    def tab_go(self, tab_name):
        mapping = {
            "dashboard": "dashboard",
            "routine": "routine",
            "budget": "budget",
            "resources": "resources",
            "events": "social",
            "settings": "settings",
        }
        self.go(mapping[tab_name])

    def _apply_font_scale(self, widget):
        scale = float(self.app.layout_scale)
        if hasattr(widget, "font_size"):
            try:
                if not hasattr(widget, "_base_font_size"):
                    widget._base_font_size = float(widget.font_size)
                widget.font_size = max(10, widget._base_font_size * scale)
            except Exception:
                pass
        if hasattr(widget, "children"):
            for c in widget.children:
                self._apply_font_scale(c)

    def _apply_theme_colors(self, widget):
        dark = bool(self.app.state.settings.get("dark_mode", False))
        is_image = widget.__class__.__name__ in {"Image", "AsyncImage", "NavIconButton"}
        if hasattr(widget, "color") and not is_image:
            try:
                color = list(widget.color)
                total = sum(color[:3])
                is_red_text = color[0] > 0.55 and color[1] < 0.30 and color[2] < 0.30
                is_nav_label = getattr(widget, "text", "") in {"Dashboard", "Routine", "Budget", "Resources", "Events", "Settings"} and total > 2.2
                is_action_on_color = hasattr(widget, "background_color") and sum(list(widget.background_color)[:3]) < 0.8
                if dark and total < 0.35 and not is_red_text:
                    widget.color = self.app.text_color
                elif not dark and total > 2.65 and not is_nav_label and not is_action_on_color:
                    widget.color = self.app.text_color
            except Exception:
                pass
        if hasattr(widget, "foreground_color"):
            try:
                widget.foreground_color = self.app.text_color
            except Exception:
                pass
        if hasattr(widget, "hint_text_color"):
            try:
                widget.hint_text_color = self.app.muted_text_color
            except Exception:
                pass
        if widget.__class__.__name__ == "TextInput":
            try:
                widget.background_color = self.app.card_color
            except Exception:
                pass
        if hasattr(widget, "children"):
            for child in widget.children:
                self._apply_theme_colors(child)

    def on_pre_enter(self, *args):
        self.active_tab = self.name if self.name in ["dashboard", "routine", "budget", "resources", "settings"] else "events" if self.name.startswith("social") else self.active_tab
        super().on_pre_enter(*args)
        self._apply_font_scale(self)
        self._apply_theme_colors(self)
